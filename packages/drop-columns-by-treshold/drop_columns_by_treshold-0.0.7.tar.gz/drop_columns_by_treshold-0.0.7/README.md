
# v0.0.7

## Суулгах:

https://pypi.org/project/drop_columns_by_treshold/

https://github.com/ganbaaelmer/drop_columns_by_treshold/tree/master/drop_columns_by_treshold

эсвэл

```

pip install drop_columns_by_treshold

```

## Ашиглах заавар:

### option1:

```

from drop_columns_by_treshold import drop_columns_by_treshold

file_name ='your_file_name.csv'

threshold = 1 # NA percent 1%

df = drop_columns_by_treshold.from_csv_filex(file_name, threshold)
```

### option2:

```
df = your_data_frame

threshold = 1 # NA percent 1%

df = df_drop_columns_by_treshold.from_dataframex(df, threshold)

```

## Үр дүн:

option1:

.csv файл уншиж уг файлаас хоосон утга ихтэй багануудыг өгөгдсөн treshold ийн %-с хамаарч устгана.

option2:

pandas dataframe-с хоосон утга ихтэй багануудыг өгөгдсөн treshold ийн %-с хамаарч устгана.

pandas dataframe df буцаана.

датаны NA-н талаар мэдээлэл харуулна

NA-н heatmap харуулна. 

