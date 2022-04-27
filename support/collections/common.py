collectList=[]
collectMDSList=[]
plotList=[]

outdir=""
from collections import *
import time as mod_time


def _run_me(session, stmt, header, file_name):
    f_output = open("{}/{}".format(outdir, file_name), 'a')

    result = session.run_sql(stmt)
    tot_cols = result.get_column_count()
    records = result.fetch_all()
    line = ""
    i = 0
    if not header:
        cols = result.get_columns()
        for col in result.get_columns():
            if i == 0:
                line = "{}".format(col.get_column_label())
            else:
                line = "{}\t{}".format(line, col.get_column_label())
            i += 1
        f_output.write(line)

    for record in records:
        i = 0
        line = ""
        while i < tot_cols:
            if i == 0:
                line = "\n{}".format(record[i])
            else:
                line = "{}\t{}".format(line, record[i])
            i += 1
        f_output.write(line)

    f_output.close()


def _generate_graph(filename, title, data, variables, type='area', stacked=False):
    import pandas as pd
    import matplotlib.pyplot as plt
    data_logs=[]
    for variable in variables:
        innodb_log = data[data['Variable_name'] == variable[0]]
        innodb_log = innodb_log.astype({'Variable_value':'int'})
        if len(variable) > 1:
           if variable[1] == 1:
              innodb_log[variable[0]] = innodb_log['Variable_value']
           else:
              innodb_log[variable[0]] = innodb_log['Variable_value']-innodb_log['Variable_value'].shift(1)
        else:
              innodb_log[variable[0]] = innodb_log['Variable_value']-innodb_log['Variable_value'].shift(1)
        data_logs.append(innodb_log)
    i = 0
    if len(data_logs) == 1:
            innodb_log = data_logs[i][['timestamp',variables[i][0]]]
    else:
        while i < len(data_logs)-1:
            if i == 0:
                innodb_log = data_logs[i][['timestamp',variables[i][0]]].merge(data_logs[i+1][['timestamp',variables[i+1][0]]])
            else:
                innodb_log = innodb_log.merge(data_logs[i+1][['timestamp',variables[i+1][0]]])
            i+=1
    #innodb_log = innodb_log.iloc[1:, :]
    ax=innodb_log.plot(kind=type,stacked=stacked, title=title, figsize=(10.24,7.68))
    file_name = "{}/{}".format(outdir, filename)
    ax.figure.savefig(file_name)
    print("Plot {} generated.".format(file_name))
    plt.close('all')
    return
