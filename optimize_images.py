
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).parent

# Логотип пока оставляем без изменений
EXCLUDE = {"logo1.png"}

converted = {}
total_old = 0
total_new = 0

# 1. Конвертируем изображения
for path in ROOT.glob("*.png"):
    if path.name in EXCLUDE:
        continue

    output = path.with_suffix(".webp")

    with Image.open(path) as img:
        img.save(output, "WEBP", quality=90, method=6)

    old_size = path.stat().st_size
    new_size = output.stat().st_size

    total_old += old_size
    total_new += new_size

    converted[path.name] = output.name

    print(
        f"{path.name}: "
        f"{old_size / 1024 / 1024:.2f} МБ -> "
        f"{new_size / 1024 / 1024:.2f} МБ"
    )

# 2. Заменяем пути в HTML и CSS
for extension in ("*.html", "*.css"):
    for file in ROOT.glob(extension):
        content = file.read_text(encoding="utf-8")

        for old_name, new_name in converted.items():
            content = content.replace(old_name, new_name)

        file.write_text(content, encoding="utf-8")

# 3. Итоги
print("\n" + "=" * 45)
print("ОПТИМИЗАЦИЯ ЗАВЕРШЕНА!")
print(f"Конвертировано изображений: {len(converted)}")
print(f"Было:  {total_old / 1024 / 1024:.2f} МБ")
print(f"Стало: {total_new / 1024 / 1024:.2f} МБ")

if total_old:
    saving = (1 - total_new / total_old) * 100
    print(f"Экономия: {saving:.1f}%")

print("\nОригинальные PNG сохранены.")
