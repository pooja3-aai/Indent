import xmlrpc.client

# Odoo server details
url = 'https://erp.michelngelo.com/'
db = 'Michelngelo'
username = 'satish@michelngelo.com'
password = 'ST'

# Common API setup
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Check authentication
if not uid:
    print("Authentication failed. Please check your credentials.")
    exit()

try:
    # Define custom fields for CRM leads
    custom_fields = [
        {'name': 'x_preferred_location', 'field_type': 'char', 'string': 'Preferred Location'},
        {'name': 'x_budget', 'field_type': 'char', 'string': 'Budget'},
        {'name': 'x_property_type', 'field_type': 'char', 'string': 'Property Type'},
        {'name': 'x_number_of_bedrooms', 'field_type': 'integer', 'string': 'Number of Bedrooms'},
        {'name': 'x_number_of_bathrooms', 'field_type': 'integer', 'string': 'Number of Bathrooms'},
        {'name': 'x_desired_amenities', 'field_type': 'char', 'string': 'Desired Amenities'},
        {'name': 'x_timeframe_for_purchase', 'field_type': 'char', 'string': 'Timeframe for Purchase'},
        {'name': 'x_investment_purpose', 'field_type': 'char', 'string': 'Investment Purpose'}
    ]

    # Get existing fields for CRM leads
    model_id = models.execute_kw(db, uid, password, 'ir.model', 'search', [[('model', '=', 'crm.lead')]])[0]
    existing_fields = models.execute_kw(db, uid, password, 'ir.model.fields', 'search_read', [[('model_id', '=', model_id)]], {'fields': ['name']})
    existing_field_names = {field['name'] for field in existing_fields}

    # Create custom fields in CRM leads
    for field in custom_fields:
        if field['name'] not in existing_field_names:
            models.execute_kw(db, uid, password, 'ir.model.fields', 'create', [{
                'model_id': model_id,
                'name': field['name'],
                'field_description': field['string'],
                'ttype': field['field_type']
            }])
            print(f"Field '{field['name']}' created successfully.")
        else:
            print(f"Field '{field['name']}' already exists.")

    # Define opportunity stages
    stages = [
        'Initial Inquiry',
        'Site Visit Scheduled',
        'Unit Reserved',
        'Sales Agreement Signed',
        'Loan Approval',
        'Final Payment',
        'Possession'
    ]

    # Create opportunity stages
    for stage in stages:
        models.execute_kw(db, uid, password, 'crm.stage', 'create', [{
            'name': stage,
            'sequence': stages.index(stage) + 1,
            'fold': False,
        }])
        print(f"Stage '{stage}' created successfully.")

    # Define custom activity types
    activity_types = [
        'Site Visit',
        'Property Presentation',
        'Follow-up Call/Email',
        'Document Submission',
        'Loan Application Follow-up'
    ]

    # Create custom activity types
    for activity_type in activity_types:
        models.execute_kw(db, uid, password, 'mail.activity.type', 'create', [{
            'name': activity_type,
        }])
        print(f"Activity type '{activity_type}' created successfully.")

    # Create CRM leads with custom fields
    leads = [
        {'name': 'Lead for 2 BHK Flat', 'contact_name': 'John Doe', 'email_from': 'john.doe@example.com',
         'phone': '1234567890', 'partner_name': 'John Doe', 'x_property_type': '2 BHK', 'x_budget': '5,000,000 - 5,500,000',
         'x_source_of_info': 'Website', 'x_visit_date': '2024-08-15', 'x_discussion_on': 'Interested in visiting', 'x_next_visit': '2024-08-20'},
        {'name': 'Lead for 4 BHK Flat', 'contact_name': 'Jane Smith', 'email_from': 'jane.smith@example.com',
         'phone': '0987654321', 'partner_name': 'Jane Smith', 'x_property_type': '4 BHK', 'x_budget': '7,000,000 - 8,000,000',
         'x_source_of_info': 'Referral', 'x_visit_date': '2024-08-16', 'x_discussion_on': 'Discussed budget and preferences', 'x_next_visit': '2024-08-22'}
    ]

    # Create CRM leads
    for lead in leads:
        try:
            models.execute_kw(db, uid, password, 'crm.lead', 'create', [{
                'name': lead['name'],
                'contact_name': lead['contact_name'],
                'email_from': lead['email_from'],
                'phone': lead['phone'],
                'partner_name': lead['partner_name'],
                'x_property_type': lead['x_property_type'],
                'x_budget': lead.get('x_budget'),
                'x_source_of_info': lead.get('x_source_of_info'),
                'x_visit_date': lead.get('x_visit_date'),
                'x_discussion_on': lead.get('x_discussion_on'),
                'x_next_visit': lead.get('x_next_visit')
            }])
            print(f"Lead '{lead['name']}' created successfully.")
        except xmlrpc.client.Fault as e:
            print(f"Error creating lead '{lead['name']}': {e}")

except xmlrpc.client.Fault as e:
    print(f"XML-RPC Fault: {e}")
except Exception as e:
    print(f"Error: {e}")
