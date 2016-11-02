from sqlalchemy import *

class Database(object):
    #engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')

    def getAbstractByTherapeuticArea(self, ta):
        engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
        con = engine.connect()
        rows = con.execute("EXECUTE [MedmemeSTG].[ups_GetAbstractForTA] @PageNo = 1,@PageSize = 300000, @TherapeuticArea='%s'" % ta)
        return_value = []
        res = rows.fetchall()
        for rowValue in res:
            abstract_id = rowValue['lngAbstractID']
            abstract_data = rowValue['txtTitle']
            return_value.append([abstract_id, abstract_data])
        con.close()
        return return_value

    def getAbstract(self):
        engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
        con = engine.connect()
        rows = con.execute('EXECUTE [MedmemeSTG].[ups_GetAbstract] @PageNo = 1,@PageSize = 100000')

        return_value = []
        res = rows.fetchall()
        for rowValue in res:
            abstract_id = rowValue['lngAbstractID']
            abstract_data = rowValue['txtTitle'] + " " + rowValue['memBody']
            return_value.append([abstract_id, abstract_data])
        con.close()
        return return_value

    def getDistinctAbstractNumber(self):
        engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
        conn = engine.connect()
        result = conn.execute("select count(distinct lngabstractID) as abstract_count from [MedmemeSTG].[tblGW]")
        row = result.fetchall()
        return row[0][0]

    def getDistinctAbstractNumberForTA(self, ta):
        engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
        conn = engine.connect()
        result = conn.execute("select count(distinct lngabstractID) as abstract_count from [MedmemeSTG].[tblGW] where  MeetingTherapeuticArea='%s'" % ta)
        row = result.fetchall()
        return row[0][0]

    def getAffiliation(self):
        engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.23:1433/Medmeme_db')
        conn = engine.connect()
        result = conn.execute("select AffiliationID, Affiliation from ReferenceData.temp_affiliation where IsProcess is null")
        return_value = []
        for rowValue in result:
            affiliation_id = rowValue['AffiliationID']
            affiliation_name = rowValue['Affiliation']
            return_value.append([affiliation_id, affiliation_name])
        conn.close()
        return return_value

    def loadTokenTable(self, total_doc, max_df, min_df):
        engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
        conn = engine.connect()
        count = 0
        return_value = []
        max_df_count = int(round(total_doc * max_df, 0))
        min_df_count = int(round(total_doc * min_df, 0))

        sql_query = "select tokenid, df from [MedmemeSTG].[GWToken_FamilyMedicineInternalMedicine] where tokenid not in (select tokenid from [MedmemeSTG].[idfListGW_FamilyMedicineInternalMedicine]) and df > {0} and df < {1}".format( min_df_count, max_df_count)
        result = conn.execute(sql_query)
        for row in result:
            count += 1
            rowValue = row
            token_id = rowValue['tokenid']
            df_value = rowValue['df']
            # therapeutic_area = rowValue['Meeting Therapeutic Area']
            return_value.append([token_id, df_value])
            if count % 1000 == 0:
                # conn.close()
                # return return_value
                print(str(count))
        conn.close()
        return return_value


    def table(self):

        engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
        conn = engine.connect()
        count=0
        return_value=[]

        result = conn.execute("SELECT TOP 5000 [lngAbstractID],[txtTitle],CONVERT(NVARCHAR(MAX), [memBody]) AS[memBody] FROM [MedmemeSTG].[tblGW] WHERE [IsProccess] IS NULL OR [IsProccess] = 0 GROUP BY[lngAbstractID], [txtTitle], CONVERT(NVARCHAR(MAX), [memBody])")
        #result = conn.execute("SELECT TOP 5000 [lngAbstractID],[txtTitle],CONVERT(NVARCHAR(MAX), [memBody]) AS[memBody] FROM [MedmemeSTG].[tblGW] WHERE [lngAbstractID]=35436869 GROUP BY[lngAbstractID], [txtTitle], CONVERT(NVARCHAR(MAX), [memBody])")
        for row in result:
            count += 1
            rowValue = row
            abstract_id = rowValue['lngAbstractID']
            abstract_data = rowValue['txtTitle']+ " "+rowValue['memBody']

            #therapeutic_area = rowValue['Meeting Therapeutic Area']
            return_value.append([abstract_id, abstract_data])
            if count%1000000==0:
                #conn.close()
                #return return_value
                print(str(count))
        conn.close()
        return return_value


    def insertToken(self, id_str, token_str, df_str, tf_str):
        try:
            engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
            conn = engine.connect()
            trans = conn.begin()
            sql = "EXECUTE MedmemeSTG.TokenInsert  @AbstractID='%s', @string=N'%s',@split='%s', @TFValue='%s', @DFValue='%s'";
            formattedSQL = sql % (id_str, token_str, ",", tf_str, df_str)
            t = text(formattedSQL).execution_options(autocommit=True)
            #result = conn.execute('EXEC [MedmemeSTG].[{MedmemeSTG}] {@{string} = "%s", @split=","}' % token_str)
            #result = conn.execute("insert into  [MedmemeSTG].[GWToken] (tokenValue, DF) values('acut','1')")

            result = conn.execute(t)
            trans.commit()
            conn.close()
        except:

            trans.rollback()  # this rolls back the transaction unconditionally
            conn.close()
            raise

    def insertTokenV1(self, id_str, token_str, df_str, tf_str):
        try:
            engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
            conn = engine.connect()
            trans = conn.begin()
            sql = "EXECUTE MedmemeSTG.TokenInsert_v1  @AbstractID='%s', @string=N'%s',@split='%s', @TFValue='%s', @DFValue='%s'";
            formattedSQL = sql % (id_str, token_str, ",", tf_str, df_str)
            t = text(formattedSQL).execution_options(autocommit=True)
            result = conn.execute(t)
            trans.commit()
            conn.close()
        except:
            trans.rollback()  # this rolls back the transaction unconditionally
            conn.close()
            raise


    def insertIdf(self, id_str, idf_str):
        try:
            engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.110:1433/CIS')
            conn = engine.connect()
            trans = conn.begin()
            sql = "EXECUTE[MedmemeSTG].[IdfInsert]  @tokenId='%s', @IDFValue='%s',@split='%s'";
            formattedSQL = sql % (id_str, idf_str, ',')
            t = text(formattedSQL).execution_options(autocommit=True)
            conn.execute("SET IDENTITY_INSERT[MedmemeSTG].[idfListGW_FamilyMedicineInternalMedicine] ON")
            result = conn.execute(t)
            trans.commit()
            conn.close()
        except:

            trans.rollback()  # this rolls back the transaction unconditionally
            conn.close()
            raise

    def insertAffiliationToken(self, id_str, token_str, split, tf_str):
        try:
            engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.23:1433/Medmeme_db')
            conn = engine.connect()
            trans = conn.begin()
            sql = "EXECUTE [ReferenceData].[InsertAffiliationToken]  @Affiliation_ID='%s', @string='%s',@split='%s', @TFValue='%s'";
            formattedSQL = sql % (id_str, token_str, ",", tf_str)
            t = text(formattedSQL).execution_options(autocommit=True)
            result = conn.execute(t)
            trans.commit()
            conn.close()
        except:
            trans.rollback()  # this rolls back the transaction unconditionally
            conn.close()
            raise

    def loadAffiliationTokens(self):
        try:
            engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.23:1433/Medmeme_db')
            conn = engine.connect()

            return_value=[]
            result = conn.execute(
                "select token_id, dfvalue as count from ReferenceData.token_idf where idfvalue is null")
            # result = conn.execute("SELECT TOP 5000 [lngAbstractID],[txtTitle],CONVERT(NVARCHAR(MAX), [memBody]) AS[memBody] FROM [MedmemeSTG].[tblGW] WHERE [lngAbstractID]=35436869 GROUP BY[lngAbstractID], [txtTitle], CONVERT(NVARCHAR(MAX), [memBody])")
            for row in result:
                rowValue = row
                token_name = rowValue['token_id']
                count = rowValue['count']

                # therapeutic_area = rowValue['Meeting Therapeutic Area']
                return_value.append([token_name, count])

            conn.close()
            return return_value
        except:
            conn.close()
            raise

    def getAffiliationCount(self):
        try:
            engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.23:1433/Medmeme_db')
            conn = engine.connect()

            return_value = []
            result = conn.execute(
                "select count(distinct AffiliationID) as affiliation_count from ReferenceData.GWAffiliationToken")
            # result = conn.execute("SELECT TOP 5000 [lngAbstractID],[txtTitle],CONVERT(NVARCHAR(MAX), [memBody]) AS[memBody] FROM [MedmemeSTG].[tblGW] WHERE [lngAbstractID]=35436869 GROUP BY[lngAbstractID], [txtTitle], CONVERT(NVARCHAR(MAX), [memBody])")
            for row in result:
                rowValue = row
                affiliation_count = rowValue['affiliation_count']
                return_value.append(affiliation_count)

            conn.close()
            return return_value[0]
        except:
            conn.close()
            raise

    def updateAffiliationIdfValue(self, token, idf):
        try:
            engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.23:1433/Medmeme_db')
            conn = engine.connect()
            return_value = []
            result = conn.execute(
                "select count(distinct AffiliationID) as affiliation_count from ReferenceData.GWAffiliationToken")
            conn.close()
        except:
            conn.close()
            raise


    def getAffiliationToken(self):
        try:
            engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.23:1433/Medmeme_db')
            conn = engine.connect()
            return_value = []
            result = conn.execute("select distinct affiliation from Medmeme_db.ReferenceData.temp_affiliation");

            for row in result:
                rowValue = row
                affiliation_count = rowValue['affiliation']
                return_value.append(affiliation_count)
            return return_value
            conn.close()
        except:
            conn.close()
            raise
