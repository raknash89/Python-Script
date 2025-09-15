from copybook import Copybook

# Sample copybook content
sample_copybook = """
01 CUSTOMER-RECORD.
   05 CUST-ID       PIC 9(5).
   05 CUST-NAME     PIC X(50).
"""

# Parse the copybook
parsed_copybook = Copybook(sample_copybook)

# Print the parsed fields
for field in parsed_copybook.fields:
    print(field.name)
    print(field.data_type)
    print(field.length)
    print("---")
