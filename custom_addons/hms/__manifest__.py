{
    'name':"HMS",
    'summary':"summary",
    'author':"Yasmeen Mohamed",
    'description':'System for Hospital Management',
    'website':'https://iti.gov.eg/home',
    'version':'0.0.2',
    'depends':['crm'],
    'data':[
        
            'views/hms_patient_views.xml',
            'views/hms_doctor_views.xml',
            'views/hms_department_views.xml',
            'views/hms_customer_inherit_view.xml',
            'security/res_groups.xml',
            'security/ir.model.access.csv',
            'reports/hms_patient_template.xml',
            'reports/reports.xml',
    ]
    
}