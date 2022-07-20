### Deprecated Functions
Select all JavaScript-Answers containing [un/escape()](https://developer.mozilla.org/de/docs/Web/JavaScript/Reference/Global_Objects/escape) function call: _javascript_m_escape.csv'_

````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<javascript>%") and body like '%<pre><code>%escape(%)%' into outfile 'javascript_m_escape.csv';
````

Select all MySQL-Answers containing [mysql_query()](https://www.php.net/manual/en/function.mysql-query.php) function call:  _mysql_m_mysql_query.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<mysql>%") and body like "%<pre><code>%mysql_query(%)%" into outfile 'mysql_m_mysql_query.csv';
````


Select all JAVA-Answers containing [addItem()](https://docs.oracle.com/javase/7/docs/api/deprecated-list.html) function call:  _java_m_addItem.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<java>%") and body like "%<pre><code>%addItem(%)%" into outfile 'java_m_addItem.csv';
````


Select all JAVA-Answers containing [appendText()](https://docs.oracle.com/javase/7/docs/api/deprecated-list.html) function call:  _java_m_appendText.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<java>%") and body like "%<pre><code>%appendText(%)%" into outfile 'java_m_appendText.csv';

````

Select all JAVA-Answers containing [classDepth()](https://docs.oracle.com/javase/7/docs/api/deprecated-list.html) function call:  _java_m_classDepth.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<java>%") and body like "%<pre><code>%classDepth(%)%" into outfile 'java_m_classDepth.csv';
````

Select all JavaScript-Answers containing [compile()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Deprecated_and_obsolete_features) function call:  _regex_m_compile.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<javascript>%") and body like "%<pre><code>%compile(%)%" into outfile 'regex_m_compile.csv';
````

Select all PHP-Answers containing is_real() function call:  _php_m_is_real.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<php>%") and body like "%<pre><code>%is_real(%)%" into outfile 'php_m_is_real.csv';
````


Select all PHP-Answers containing restore_include_path() function call:  _php_m_restore_include_path.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<php>%") and body like "%<pre><code>%restore_include_path(%)%" into outfile 'php_m_restore_include_path.csv';
````


Select all C-Answers containing atol() function call:  _c_m_atol.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<c>%") and body like "%<pre><code>%atol(%)%" into outfile 'c_m_atol.csv';

````

Select all C-Answers containing ctime() function call:  _c_m_ctime.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<c>%") and body like "%<pre><code>%ctime(%)%" into outfile 'c_m_ctime.csv';
````

Select all C-Answers containing setbuf() function call:  _c_m_setbuf.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<c>%") and body like "%<pre><code>%setbuf(%)%" into outfile 'c_m_setbuf.csv';
````


Select all Python-Answers containing clock() function call:  _python_m_clock.csv_
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<python>%") and body like "%<pre><code>%clock(&)%" into outfile 'python_m_clock.csv';
````
### SQL-Injection
Based on [https://github.com/laurent22/so-sql-injections/blob/master/src/AppBundle/InjectionFinder.php](https://github.com/laurent22/so-sql-injections/blob/master/src/AppBundle/InjectionFinder.php):  
sql-injection1.csv
````sql
Select id From posts where body REGEXP "SELECT[[:blank:]]+.*[[:blank:]]FROM[[:blank:]]*[[:blank:]]WHERE[[:blank:]].*[$][a-zA-Z_].*";
````
sql-injection2.csv
````sql
Select id From posts where body REGEXP "SELECT[[:blank:]]+.*[$][a-zA-Z_].*[[:blank:]]FROM.*";
````
sql-injection3.1.csv - sql-injection3.5.csv
````sql
Select id From posts where body REGEXP "INSERT[[:blank:]]+INTO[[:blank:]].*[$][a-zA-Z_].*";
````
sql-injection4.1.csv, sql-injection4.2.csv
````sql
Select id From posts where body REGEXP "UPDATE[[:blank:]]+.*[[:blank:]]SET[[:blank:]].*[$][a-zA-Z_].*";
````
sql-injection5.csv
````sql
Select id From posts where body REGEXP "DELETE[[:blank:]]+FROM[[:blank:]]+.*[$][a-zA-Z_].*";
````  
### Remote Code Execution (RCE)  
PHP RCE php_exec_rce.csv
````sql
Select id From posts where id in (select p2.id from posts p1 INNER JOIN posts p2 ON p2.ParentId = p1.Id Where p1.tags like "%<php>%") and body like "%<pre><code>% exec(%$%)%" into outfile 'php_exec_rce.csv';
````