import os

# Ler o arquivo
with open('lockerscreens.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Corrigir ambos os botões para garantir background amarelo
content = content.replace(
    'background_color=(0, 0, 0, 0)  # Transparent default background',
    'background_color=(1, 204/255, 0, 1)  # Yellow background directly'
)

# Reduzir espaço removendo o Widget expansível
content = content.replace(
    'content_scroll.add_widget(Widget(size_hint_y=1))  # This will expand to fill space',
    'content_scroll.add_widget(Widget(size_hint_y=None, height=dp(30)))  # Small fixed spacing'
)

# Salvar
with open('lockerscreens.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Cores corrigidas e espaço reduzido!")