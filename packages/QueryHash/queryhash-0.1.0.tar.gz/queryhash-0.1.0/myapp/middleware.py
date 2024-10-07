# myapp/middleware.py

import hashlib
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from .models import HashRecord

class QueryResponseHashMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # Get the query from the request (e.g., from a query parameter)
        query = request.GET.get('query', None)  # Example: /your-url/?query=SELECT * FROM job

        if query:
            # Execute the query
            with connection.cursor() as cursor:
                cursor.execute(query)
                query_response = cursor.fetchall()

            # Convert response to string for hashing
            response_str = str(query_response)
            import pdb;pdb.set_trace()
            # Hash the query and response
            query_hash = hashlib.sha256(query.encode()).hexdigest()
            response_hash = hashlib.sha256(response_str.encode()).hexdigest()

            # Store in the database if both hashes are different
            try:
                hash_record = HashRecord.objects.get(query_hash=query_hash, response_hash=response_hash)
                # If they are the same, increment the count
                hash_record.count += 1
                hash_record.save()
            except HashRecord.DoesNotExist:
                # Create a new record if it does not exist
                HashRecord.objects.create(query=query, query_hash=query_hash, response_hash=response_hash)

        return response
