# v0.0.2

## Суулгах:

https://pypi.org/project/drop_columns_by_treshold/

https://github.com/ganbaaelmer/drop_columns_by_treshold/tree/master/drop_columns_by_treshold

эсвэл

```

pip install drop_columns_by_treshold

```

## Ашиглах заавар:

```

from drop_columns_by_treshold import drop_columns_by_treshold

fileName ='your_file_name.csv'

threshold = 0.1

df = drop_columns_by_treshold.drop_columns_by_treshold(file_name, threshold)

```

## үр дүн:

.csv файл уншиж уг файлаас хоосон утга ихтэй багануудыг өгөгдсөн treshold ийн %-с хамаарч устгана.

pandas dataframe df буцаана.

датаны NA-н талаар мэдээлэл харуулна

NA-н heatmap харуулна. 
