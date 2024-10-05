from setuptools import setup, find_packages

setup(
    name="uzpy",
    version="0.8",
    packages=find_packages(),
    install_requires=["datetime"],  
    description = """O'zbek tilidagi Python kutubxonasi

O'zbek tilida Python dasturlash tilini o'rganishni va rivojlantirishni maqsad qilgan kutubxona. Ushbu kutubxona Python dasturlash tilida o'zbek tilida resurslar, qo'llanmalar va funksiyalarni taqdim etadi. Dasturchilar uchun qulaylik yaratish va dasturlashni yanada ommalashtirish uchun yaratilgan.

- **Maqsad**: Python dasturlash tilini o'zbek tilida o'rgatish va dasturlashni osonlashtirish.
- **Faoliyatlar**: O'zbek tilida Python qo'llanmalari, kutubxonalar va o'quv materiallari yaratish.
- **Yordam**: Dasturchilar va o'qituvchilar uchun o'zbek tilida maxsus resurslar va qo'llanmalar.

Ko'proq ma'lumot uchun biz bilan bog'laning.""",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  
    author="Qaxxorov DEVV",
    url="https://www.youtube.com/@qaxxorovdevv",  
)
