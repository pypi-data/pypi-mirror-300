import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-endpoints",
    version="0.0.2",
    author="xlartas",
    author_email="ivanhvalevskey@gmail.com",
    description="Package to display all URLs of a Django application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Artasov/django-endpoints",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.0,<5.3",
    ],
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires='>=3.8',
    keywords='django urls endpoints',
    project_urls={
        'Source': 'https://github.com/Artasov/django-endpoints',
        'Tracker': 'https://github.com/Artasov/django-endpoints/issues',
    },
)
