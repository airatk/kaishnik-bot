from typing import List
from typing import Tuple

from bot.utilities.api.constants import SCORE_TEMPLATE


def beautify_score(raw_score_table_data: List[List[str]]) -> List[Tuple[str, str]]:
	# Slightly refining traditional assessment to be written starting with lower case letter
	for (subject_index, subject_score_data) in enumerate(raw_score_table_data):
		# Making traditional grade to be viewed in the lower case
		subject_score_data[16] = subject_score_data[16].lower()

		# Putting strikethrough text decoration on non-grade value
		if subject_score_data[16] == "ведомость не закрыта":
			subject_score_data[16] = f"~{subject_score_data[16]}~"

		# Finishing traditional grade processing
		raw_score_table_data[subject_index][16] = subject_score_data[16]

	score: List[Tuple[str, str]] = []

	for subject_score_data in raw_score_table_data:
		formatted_subject_score_data: str = SCORE_TEMPLATE.format(*subject_score_data[1:])

		# Preparing for parsing by Markdown Parser of Version 2
		for reserved_character in [ "-", "(", ")", "." ]:
			formatted_subject_score_data = formatted_subject_score_data.replace(reserved_character, f"\{reserved_character}")

		# Enhancing some words' appearance
		formatted_subject_score_data = formatted_subject_score_data.replace("н/я", "неявка")

		score.append((subject_score_data[1], formatted_subject_score_data))
	
	return score
