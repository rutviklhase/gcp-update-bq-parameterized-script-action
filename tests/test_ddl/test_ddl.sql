CREATE OR REPLACE VIEW
  output.table_name
 AS
SELECT
	 column_name_1 as cn_1
	,column_name_2 as cn_2
	,column_name_3 as cn_3
	,column_name_4 as cn_4
	,column_name_5 as cn_5
	,column_name_6 as cn_6
	,column_name_7 as cn_7
	,created_datetime
	,modified_datetime
FROM
  `{{PROJECT_ID}}.database.table_name`
