from setuptools import find_packages, setup

with open("library.md", "r") as f:
    long_description = f.read()

setup(
    name="speechlib",
    version="1.1.10",  
    description="speechlib is a library that can do speaker diarization, transcription and speaker recognition on an audio file to create transcripts with actual speaker names. This library also contain audio preprocessor functions.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NavodPeiris/speechlib",
    author="Navod Peiris",
    author_email="navodpeiris1234@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["transformers>=4.36.2, <5.0.0", "torch>=2.1.2, <3.0.0", "torchaudio>=2.1.2, <3.0.0", "pydub>=0.25.1, <1.0.0", "pyannote.audio>=3.1.1, <4.0.0", "speechbrain>=0.5.16, <1.0.0", "accelerate>=0.26.1, <1.0.0", "faster-whisper>=0.10.1, <1.0.0", "openai-whisper>=20231117, <20240927", "assemblyai"],
    python_requires=">=3.8",
)

# ["transformers==4.36.2", "torch==2.1.2", "torchaudio==2.1.2", "pydub==0.25.1", "pyannote.audio==3.1.1", "speechbrain==0.5.16", "accelerate==0.26.1", "faster-whisper==0.10.1", "openai-whisper==20231117"]