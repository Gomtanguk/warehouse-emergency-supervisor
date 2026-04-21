from glob import glob
from setuptools import setup


package_name = "warehouse_emergency_supervisor"


setup(
    name=package_name,
    version="0.1.0",
    py_modules=["integrated_warehouse_supervisor_v6"],
    packages=["custom_mobile"],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/assets", glob("*.usd") + ["map.png", "map.yaml", "Readme.md", "robotiq_2f_140.zip"]),
        (f"share/{package_name}/assets/barcodes", glob("barcodes/*.png")),
    ],
    install_requires=["setuptools"],
    zip_safe=False,
    maintainer="Gomtanguk",
    maintainer_email="gomtanguk@example.com",
    description="Isaac Sim and ROS 2 integrated warehouse emergency supervisor.",
    license="Proprietary",
    entry_points={
        "console_scripts": [
            "warehouse_supervisor = integrated_warehouse_supervisor_v6:main",
        ],
    },
)
