from typing import List, Optional, Dict, Union
from ..errors.exceptions import CustomException
from ..database import DatabaseManager
from ..api_keys.neuraltrust_api_key import NeuralTrustApiKey
import json
import time

class NeuralTrustApiService:
    @staticmethod
    def _get_app_id():
        neuraltrust_app_id = NeuralTrustApiKey.get_app_id()
        return neuraltrust_app_id

    @staticmethod
    def firewall(input: str):
        """
        Checks the input text against firewall rules in the database.
        """
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM firewall_rules WHERE %s LIKE pattern", (input,))
                    result = cur.fetchone()
                return {"allowed": result is None}
            except Exception as e:
                raise CustomException("Firewall check failed", str(e))

    @staticmethod
    def create_testset(testset: List[Dict]):
        """
        Creates a testset in the database.
        """
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    # Insert each testset row individually
                    for row in testset:
                        cur.execute(
                            'INSERT INTO "Testsets" ("id", "appId", "testsetId", "evaluationSetId", "query", "context", "expectedResponse", "conversationHistory", "metadata") '
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                            (
                                row.get('id'),
                                NeuralTrustApiService._get_app_id(),
                                row.get('testsetId'),
                                row.get('evaluationSetId'),
                                row.get('query'),
                                json.dumps(row.get('context')),
                                row.get('expectedResponse'),
                                json.dumps(row.get('conversationHistory')),
                                json.dumps(row.get('metadata'))
                            )
                        )
                conn.commit()
                return {"message": f"Successfully created {len(testset)} testset rows"}
            except Exception as e:
                conn.rollback()
                raise CustomException("Failed to create testset", str(e))

    @staticmethod
    def update_testset(testset_id: str, update_data: Dict):
        """
        Updates a testset in the database.
        """
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute('UPDATE "Testsets" SET data = data || %s::jsonb WHERE id = %s RETURNING id;', (json.dumps(update_data), testset_id))
                    updated_id = cur.fetchone()[0]
                conn.commit()
                return {"id": updated_id}
            except Exception as e:
                conn.rollback()
                raise CustomException("Failed to update testset", str(e))

    @staticmethod
    def create_evaluation_set(evaluation_set_data: Dict):
        """
        Creates a new evaluation set in the database.
        Only accepts specific fields and filters out any unexpected data.
        """
        allowed_fields = {
            'id', 'appId', 'name', 'testsetId', 'status', 'description', 'scheduler', 'numQuestions'
        }
        evaluation_set_data["appId"] = NeuralTrustApiService._get_app_id()
        filtered_data = {k: v for k, v in evaluation_set_data.items() if k in allowed_fields}
        
        if not filtered_data.get('id') or not filtered_data.get('name'):
            raise CustomException("Failed to create evaluation set", "Missing required fields: 'id' and 'name'")

        with DatabaseManager.get_connection() as conn:
            try:
                columns = ', '.join(f'"{k}"' for k in filtered_data.keys())
                placeholders = ', '.join('%s' for _ in filtered_data)
                values = list(filtered_data.values())
                
                query = f'INSERT INTO "EvaluationSets" ({columns}) VALUES ({placeholders}) RETURNING id;'
                with conn.cursor() as cur:
                    cur.execute(query, values)
                    eval_set_id = cur.fetchone()[0]
                conn.commit()
                return {"id": eval_set_id}
            except Exception as e:
                conn.rollback()
                raise CustomException("Failed to create evaluation set", str(e))

    @staticmethod
    def update_evaluation_set(evaluation_set_id: str, update_data: Dict):
        """
        Updates an existing evaluation set in the database.
        Only accepts specific fields and filters out any unexpected data.
        """
        allowed_fields = {
            'name', 'testsetId', 'status', 'description', 'scheduler', 'numQuestions', 'numFailed', 'numTests', 'avgPassed', 'numPassed', 'lastRunAt', 'nextRunAt'
        }
        filtered_data = {k: v for k, v in update_data.items() if k in allowed_fields}
        
        if not filtered_data:
            raise CustomException("Failed to update evaluation set", "No valid fields to update")

        with DatabaseManager.get_connection() as conn:
            try:
                set_clause = ', '.join(f'"{k}" = %s' for k in filtered_data.keys())
                query = f'UPDATE "EvaluationSets" SET {set_clause} WHERE id = %s RETURNING id;'
                values = list(filtered_data.values()) + [evaluation_set_id]
                with conn.cursor() as cur:
                    cur.execute(query, values)
                    updated_id = cur.fetchone()[0]
                conn.commit()
                return {"id": updated_id}
            except Exception as e:
                conn.rollback()
                raise CustomException("Failed to update evaluation set", str(e))

    @staticmethod
    def load_evaluation_set(evaluation_set_id: str):
        """
        Loads an existing evaluation set from the database.
        """
        print(f"Loading evaluation set with ID: {evaluation_set_id}")
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute('SELECT * FROM "EvaluationSets" WHERE id = %s;', (evaluation_set_id,))
                    result = cur.fetchone()
                    if result and cur.description:
                        columns = [desc[0] for desc in cur.description]
                        return dict(zip(columns, result))
                    else:
                        print(f"No evaluation set found with ID: {evaluation_set_id}")
                        return None
            except Exception as e:
                print(f"Error loading evaluation set: {str(e)}")
                raise CustomException("Failed to load evaluation set", str(e))
    @staticmethod
    def load_api_config():
        """
        Loads API configuration from the database.
        """
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute('SELECT "evaluationEndpoint" FROM "App" WHERE id = %s;', (NeuralTrustApiService._get_app_id(),))
                    result = cur.fetchone()
                    if result:
                        return {"evaluationEndpoint": result[0]}
                    else:
                        print("No API configuration found in the database.")
                        return {"evaluationEndpoint": ""}  # Return a default configuration
            except Exception as e:
                print(f"Error loading API config: {str(e)}")
                return {"evaluationEndpoint": ""}  # Return a default configuration on error

    @staticmethod
    def fetch_testset_rows(
            testset_id: str,
            number_of_rows: Optional[int] = None,
            max_retries: int = 3,
            retry_delay: int = 5
    ):
        """
        Fetch the testset rows from the database
        """
        if number_of_rows is None:
            number_of_rows = 500

        for attempt in range(max_retries):
            with DatabaseManager.get_connection() as conn:
                try:
                    with conn.cursor() as cur:
                        cur.execute("""
                        SELECT * FROM "Testsets"
                        WHERE "testsetId" = %s
                        LIMIT %s
                        """, (testset_id, number_of_rows))
                        rows = cur.fetchall()
                        columns = [desc[0] for desc in cur.description]
                        result = []
                        for row in rows:
                            row_dict = dict(zip(columns, row))
                            row_dict['expected_response'] = row_dict.pop('expectedResponse', None)
                            row_dict['evaluation_set_id'] = row_dict.pop('evaluationSetId', None)
                            row_dict['testset_id'] = row_dict.pop('testsetId', None)
                            row_dict['conversation_history'] = row_dict.pop('conversationHistory', None)
                            result.append(row_dict)
                        return result
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"Error fetching testset rows: {str(e)}. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        raise CustomException("Failed to load testset from database", str(e))

        raise CustomException("Max retries reached", "Failed to fetch testset rows after multiple attempts")

    @staticmethod
    def log_eval_details(eval_results: Union[dict, List[dict]]):
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    if isinstance(eval_results, dict):
                        eval_results = [eval_results]
                    
                    app_id = NeuralTrustApiService._get_app_id()
                    
                    for result in eval_results:
                        # Add appId to each result
                        result['appId'] = app_id
                        
                        columns = ', '.join(f'"{k}"' for k in result.keys())
                        placeholders = ', '.join(['%s'] * len(result))
                        values = tuple(result.values())
                        
                        query = f'INSERT INTO "EvaluationRunsDetails" ({columns}) VALUES ({placeholders}) RETURNING id;'
                        cur.execute(query, values)
                    
                    conn.commit()
                return {"status": "success"}
            except Exception as e:
                conn.rollback()
                raise CustomException("Failed to log evaluation details", str(e))

    @staticmethod
    def log_eval_run(eval_run: dict):
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    # Add appId to the eval_run dictionary
                    eval_run['appId'] = NeuralTrustApiService._get_app_id()
                    
                    columns = ', '.join(f'"{k}"' for k in eval_run.keys())
                    placeholders = ', '.join(['%s'] * len(eval_run))
                    values = tuple(eval_run.values())
                    
                    query = f'INSERT INTO "EvaluationRuns" ({columns}) VALUES ({placeholders}) RETURNING id;'
                    cur.execute(query, values)
                    run_id = cur.fetchone()[0]
                conn.commit()
                return {"id": run_id}
            except Exception as e:
                conn.rollback()
                raise CustomException("Failed to log evaluation run", str(e))

    @staticmethod
    def update_testsets(testsets: List[Dict]):
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    for testset in testsets:
                        # Update the query to match the actual table structure
                        # Assuming we want to update all fields in the testset
                        update_fields = ', '.join([f'"{key}" = %s' for key in testset.keys() if key != 'id'])
                        values = [testset[key] for key in testset.keys() if key != 'id']
                        values.append(testset['id'])
                        
                        query = f'UPDATE "Testsets" SET {update_fields} WHERE id = %s'
                        cur.execute(query, values)
                conn.commit()
                return {"status": "success"}
            except Exception as e:
                conn.rollback()
                raise CustomException("Failed to update testsets", str(e))