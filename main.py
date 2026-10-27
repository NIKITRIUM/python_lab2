coffe_csv = open('Coffe_sales.csv')
A = [i for i in coffe_csv]
coffe_csv.close()
print(A[:10])