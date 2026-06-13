import pymysql

# This tricks Django into thinking mysqlclient is installed
pymysql.version_info = (2, 2, 8, "final", 0)
pymysql.install_as_MySQLdb()
