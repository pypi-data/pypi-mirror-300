from setuptools import setup, find_packages


setup(
    name="speech_text_pipeline",
    version="0.0.1",
    author="Arya Shukla",
    author_email="aryashukla95@gmail.com",
    description="A speech transcription and speaker diarization pipeline, with speaker matching for know speaker",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aryashukla/speech_text_pipeline",
    packages=find_packages(),
    install_requires=[
        "transformers",
        "numpy",
        "scipy",
        "librosa",
        "lhotse",
        "jiwer",
        "webdataset",
        "soundfile",
        "wget",
        "ipython",
        "torch",
        "triton",
        "nvidia-cublas-cu11==11.10.3.66",
        "nvidia-cuda-cupti-cu11==11.7.101",
        "nvidia-cuda-nvrtc-cu11==11.7.99",
        "nvidia-cuda-runtime-cu11==11.7.99",
        "nvidia-cudnn-cu11==8.5.0.96"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)