"""
Podcastfy CLI

This module provides a command-line interface for generating podcasts or transcripts
from URLs or existing transcript files. It orchestrates the content extraction,
generation, and text-to-speech conversion processes.
"""
import os
import uuid
import typer
from podcastfy.content_parser.content_extractor import ContentExtractor
from podcastfy.content_generator import ContentGenerator
from podcastfy.text_to_speech import TextToSpeech
from podcastfy.utils.config import Config, load_config
from podcastfy.utils.logger import setup_logger
from typing import List, Optional, Dict, Any
import copy


logger = setup_logger(__name__)

app = typer.Typer()


def process_links(links, transcript_file=None, tts_model="openai", generate_audio=True, config=None):
    """
    Process a list of links or a transcript file to generate a podcast or transcript.

    Args:
            links (list): A list of URLs to process.
            transcript_file (str): Path to a transcript file (optional).
            tts_model (str): The TTS model to use ('openai' or 'elevenlabs'). Defaults to 'openai'.
            generate_audio (bool): Whether to generate audio or just a transcript. Defaults to True.
            config (Config): Configuration object to use. If None, default config will be loaded.

    Returns:
            str: Path to the final podcast audio file or transcript file.
    """
    try:
        if config is None:
            config = load_config()

        if transcript_file:
            logger.info(f"Using transcript file: {transcript_file}")
            with open(transcript_file, "r") as file:
                qa_content = file.read()
        else:
            logger.info(f"Processing {len(links)} links")
            content_extractor = ContentExtractor(config.JINA_API_KEY)
            content_generator = ContentGenerator(config.GEMINI_API_KEY)

            # Extract content from links
            contents = [content_extractor.extract_content(link) for link in links]

            # Combine all extracted content
            combined_content = "\n\n".join(contents)

            # Generate Q&A content
            random_filename = f"transcript_{uuid.uuid4().hex}.txt"
            output_filepath = os.path.join(config.get('output_directories')['transcripts'], random_filename)
            qa_content = content_generator.generate_qa_content(
                combined_content, output_filepath=output_filepath
            )

        if generate_audio:
            text_to_speech = TextToSpeech(
                model=tts_model, api_key=getattr(config, f"{tts_model.upper()}_API_KEY")
            )
            # Convert text to speech using the specified model
            random_filename = f"podcast_{uuid.uuid4().hex}.mp3"
            audio_file = os.path.join(config.get('output_directories')['audio'], random_filename)
            text_to_speech.convert_to_speech(qa_content, audio_file)
            logger.info(f"Podcast generated successfully using {tts_model} TTS model")
            return audio_file
        else:
            logger.info(f"Transcript generated successfully")
            return output_filepath

    except Exception as e:
        logger.error(f"An error occurred in the process_links function: {str(e)}")
        raise


@app.command()
def main(
    urls: list[str] = typer.Option(None, "--url", "-u", help="URLs to process"),
    file: typer.FileText = typer.Option(
        None, "--file", "-f", help="File containing URLs, one per line"
    ),
    transcript: typer.FileText = typer.Option(
        None, "--transcript", "-t", help="Path to a transcript file"
    ),
    tts_model: str = typer.Option(
        None, "--tts-model", "-tts", help="TTS model to use (openai or elevenlabs)"
    ),
    transcript_only: bool = typer.Option(
        False, "--transcript-only", help="Generate only a transcript without audio"
    ),
):
    """
    Generate a podcast or transcript from a list of URLs, a file containing URLs, or a transcript file.
    """
    try:
        config = load_config()
        main_config = config.get('main', {})

        # Use default TTS model from config if not specified
        if tts_model is None:
            tts_model = main_config.get('default_tts_model', 'openai')

        if transcript:
            final_output = process_links(
                [],
                transcript_file=transcript.name,
                tts_model=tts_model,
                generate_audio=not transcript_only,
            )
        else:
            urls_list = urls or []
            if file:
                urls_list.extend([line.strip() for line in file if line.strip()])

            if not urls_list:
                raise typer.BadParameter(
                    "No URLs provided. Use --url to specify URLs, --file to specify a file containing URLs, or --transcript for a transcript file."
                )

            final_output = process_links(
                urls_list, tts_model=tts_model, generate_audio=not transcript_only
            )

        if transcript_only:
            typer.echo(f"Transcript generated successfully: {final_output}")
        else:
            typer.echo(
                f"Podcast generated successfully using {tts_model} TTS model: {final_output}"
            )

    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
    


def generate_podcast(
	urls: Optional[List[str]] = None,
	url_file: Optional[str] = None,
	transcript_file: Optional[str] = None,
	tts_model: Optional[str] = None,
	transcript_only: bool = False,
	config: Optional[Dict[str, Any]] = None
) -> str:
	"""
	Generate a podcast or transcript from a list of URLs, a file containing URLs, or a transcript file.

	Args:
		urls (Optional[List[str]]): List of URLs to process.
		url_file (Optional[str]): Path to a file containing URLs, one per line.
		transcript_file (Optional[str]): Path to a transcript file.
		tts_model (Optional[str]): TTS model to use ('openai' or 'elevenlabs').
		transcript_only (bool): Generate only a transcript without audio. Defaults to False.
		config (Optional[Dict[str, Any]]): User-provided configuration dictionary.

	Returns:
		str: Path to the final podcast audio file or transcript file.

	Example:
		>>> from podcastfy.client import generate_podcast
		>>> result = generate_podcast(
		...     urls=['https://example.com/article1', 'https://example.com/article2'],
		...     tts_model='elevenlabs',
		...     config={
		...         'main': {
		...             'default_tts_model': 'elevenlabs'
		...         },
		...         'output_directories': {
		...             'audio': '/custom/path/to/audio',
		...             'transcripts': '/custom/path/to/transcripts'
		...         }
		...     }
		... )
	"""
	try:
		# Load default config
		default_config = load_config()

		# Update config if provided
		if config:
			if isinstance(config, dict):
				# Create a deep copy of the default config
				updated_config = copy.deepcopy(default_config)
				# Update the copy with user-provided values
				updated_config.configure(**config)
				default_config = updated_config
			elif isinstance(config, Config):
				# If it's already a Config object, use it directly
				default_config = config
			else:
				raise ValueError("Config must be either a dictionary or a Config object")

		main_config = default_config.config.get('main', {})

		# Use provided tts_model if specified, otherwise use the one from config
		if tts_model is None:
			tts_model = main_config.get('default_tts_model', 'openai')

		if transcript_file:
			return process_links(
				[],
				transcript_file=transcript_file,
				tts_model=tts_model,
				generate_audio=not transcript_only,
				config=default_config
			)
		else:
			urls_list = urls or []
			if url_file:
				with open(url_file, 'r') as file:
					urls_list.extend([line.strip() for line in file if line.strip()])

			if not urls_list:
				raise ValueError(
					"No URLs provided. Please provide either 'urls', 'url_file', or 'transcript_file'."
				)

			return process_links(
				urls_list, 
				tts_model=tts_model, 
				generate_audio=not transcript_only,
				config=default_config
			)

	except Exception as e:
		logger.error(f"An error occurred: {str(e)}")
		raise