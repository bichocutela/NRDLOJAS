import re
with open('app/src/main/java/com/example/data/ProductDao.kt', 'r') as f:
    content = f.read()

content = content.replace('@Insert(onConflict = OnConflictStrategy.REPLACE)\n    @Delete\n    suspend fun deleteProduct', '@Delete\n    suspend fun deleteProduct')

with open('app/src/main/java/com/example/data/ProductDao.kt', 'w') as f:
    f.write(content)
print("Fixed ProductDao")
