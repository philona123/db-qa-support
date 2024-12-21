import streamlit as st

from vanna.remote import VannaDefault

vn = None

@st.cache_resource(ttl=3600)
def setup_vanna():
    # # vn = VannaDefault(api_key=st.secrets.get("VANNA_API_KEY"), model='chinook')
    # api_key = "f4a685108e044b1389e2a58302777739"
    # vanna_model_name = "qasupport"
    # vn = VannaDefault(model=vanna_model_name, api_key=api_key)
    # vn.connect_to_postgres(host='localhost', dbname='clinic_cloud', user='postgres', password='postgres', port='5432')
    # df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
    # plan = vn.get_training_plan_generic(df_information_schema)
    # vn.train(plan=plan)
    # return vn
    global vn
    if vn is None:
        api_key = st.secrets["API_KEY"]
        vanna_model_name = st.secrets["MODEL_NAME"]
        vn = VannaDefault(model=vanna_model_name, api_key=api_key)
        vn.connect_to_postgres(
            host=st.secrets['POSTGRES_HOST'], 
            dbname=st.secrets['POSTGRES_DB'], 
            user=st.secrets['POSTGRES_USER'], 
            password=st.secrets['POSTGRES_PASSWORD'], 
            port=st.secrets['POSTGRES_PORT'], 
        )
        vn.train(documentation="""
                    The database do not have foreign keys concepts but there is relationships between tables. Some of the relationships are:
                    the treatmentPlanVersionId column in aligner_production table corresponds to the id of the treatment_plan_version table. The treatmentId in aligner_production table corresponds to the id of the treatment table. The treatmentPlanId column in the aligner_production table corresponds to the id of the treatment_plan table.
                    the clinicId in the clinic_details table corresponds to the id of the clinic table.
                    the clinicId in the clinic_tier table corresponds to the id of the clinic table.
                    the name column in the group table also means role or user role.
                    the groupId column in the group_permission table corresponds to the id of the group table.
                    the permissionId column in the group permission table corresponds to the id of the permission table.
                    the userId in the leave table corresponds to the id of the user table.
                    the relatedId in the note table can correspond to any id of other tables.
                    the noteId in the note_document table corresponds to the id of the note table.
                    the documentId in the note_document table corresponds to the id of the document table.
                    the userId in the patient_details table corresponds to the id of the user table.
                    the patientId in the patient_guardian table corresponds to the id of the user table and also the userId in the patient_details table.
                    the clinicId in the quote table corresponds to the id of the clinic table.
                    the quoteId in the quote_line table corresponds to the id of the quote table.
                    the patientId in the quote_line table corresponds to the id of the user table.
                    the doctorId in the quote_line table corresponds to the id of the user table.
                    the quoteId in the quote_line_proposal table corresponds to the id of the quote table.
                    the quoteLineId in the quote_line_proposal table corresponds to the id of the quote_line table.
                    the clinicId in the referral table corresponds to the id of the clinic table.
                    the referringStaffId in the referral table corresponds to the id of the user table.
                    the patientId in the referral table corresponds to the id of the user table.
                    the referralId in the referral_document table corresponds to the id of the referral table.
                    the staffId in the staff_assign_config table corresponds to the id of the user table.
                    the staffId in the staff_capacity table corresponds to the id of the user table.
                    the userId in the staff_details table corresponds to the id of the user table.
                """) 
        vn.train(documentation="role mean name in the group table")
        vn.train(question="What are the permission available for the role SUPER_ADMIN?", 
                sql='''select p."name" as permission_name 
                      from group_permission gp 
                      left join "permission" p on gp."permissionId" = p.id 
                      left join "group" g on g.id = gp."groupId" 
                      where g."name" = 'SUPER_ADMIN' ''')
        vn.train(documentation='''Since some of column names are camel case, we need to reference the column as object.columnName for example gp."groupId"''')
        # Optionally add schema hints
        # vn.add_context("The database has tables: 'treatment', 'patients', 'appointments'. Use correct table names.")
    return vn
print("setup_vanna calling")
vn = setup_vanna()

@st.cache_data(show_spinner="Generating sample questions ...")
def generate_questions_cached():
    # vn = setup_vanna()
    return vn.generate_questions()


@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str):
    # vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)

@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str):
    # vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)

@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str):
    # vn = setup_vanna()
    return vn.run_sql(sql=sql)

@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df):
    # vn = setup_vanna()
    return vn.should_generate_chart(df=df)

@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df):
    # vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df):
    # vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)


@st.cache_data(show_spinner="Generating followup questions ...")
def generate_followup_cached(question, sql, df):
    # vn = setup_vanna()
    return vn.generate_followup_questions(question=question, sql=sql, df=df)

@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(question, df):
    # vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)