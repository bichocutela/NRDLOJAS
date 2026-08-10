import re
content = open("app/src/main/java/com/example/ui/MainViewModel.kt").read()

target = r"""        \} else \{
            repository\.insertProduct\(product\)
            _syncMessage\.emit\("Salvo apenas localmente \(Nuvem não configurada\)"\)
            _newProductsCount\.value \+= 1
            return true
        \}"""

replacement = """        } else {
            _syncMessage.emit("Não foi possível publicar o produto. Verifique a conexão e tente novamente.")
            return false
        }"""

content = re.sub(target, replacement, content)
open("app/src/main/java/com/example/ui/MainViewModel.kt", "w").write(content)
print("Success")
