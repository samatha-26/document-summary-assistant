from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import re
from collections import Counter

# Download necessary NLTK data if not already downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def extract_key_topics(text, num_topics=5):
    """Extract key topics from the text using frequency analysis."""
    # Tokenize and clean
    words = nltk.word_tokenize(text.lower())
    stop_words = set(nltk.corpus.stopwords.words('english'))
    stop_words.update(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'])

    # Filter words
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words and len(word) > 3]

    # Get most common words
    word_freq = Counter(filtered_words)
    return [word for word, _ in word_freq.most_common(num_topics)]

def generate_structured_summary(text):
    """
    Generate a structured summary with title, introduction, and organized sections.

    Args:
        text (str): The text to summarize.

    Returns:
        str: The structured summary.
    """
    if not text.strip():
        return "No text available to summarize."

    # Extract title from first meaningful sentence
    sentences = nltk.sent_tokenize(text)
    title_candidates = [s.strip() for s in sentences[:3] if len(s.split()) > 3]
    title = title_candidates[0] if title_candidates else "Document Summary"

    # Clean title
    title = re.sub(r'^[^\w]*', '', title)  # Remove leading non-word chars
    title = title.split('.')[0].strip()  # Take first sentence
    if len(title) > 50:
        title = title[:47] + "..."

    # Get key topics
    topics = extract_key_topics(text, 4)

    # Generate summary sentences using TextRank
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")

    summary_sentences = summarizer(parser.document, 8)  # Get more sentences for structuring

    # Extract and clean sentences
    sentences = [str(sentence).strip() for sentence in summary_sentences]

    # Remove duplicates and clean
    seen = set()
    unique_sentences = []
    for sentence in sentences:
        normalized = re.sub(r'\s+', ' ', sentence.lower().strip())
        if normalized not in seen and len(normalized) > 15:
            seen.add(normalized)
            unique_sentences.append(sentence)

    # Structure the summary
    structured_summary = f"Summary: {title}\n\n"

    # Introduction (first 1-2 sentences)
    intro_sentences = unique_sentences[:2]
    intro = '. '.join(intro_sentences)
    if intro and not intro.endswith('.'):
        intro += '.'
    structured_summary += intro + "\n\n"

    # Organize remaining content by topics
    remaining_sentences = unique_sentences[2:]
    if topics and remaining_sentences:
        section_num = 1
        for topic in topics:
            # Find sentences related to this topic
            topic_sentences = []
            for sentence in remaining_sentences:
                if topic.lower() in sentence.lower():
                    topic_sentences.append(sentence)
                    remaining_sentences.remove(sentence)

            if topic_sentences:
                structured_summary += f"{section_num}. {topic.title()}\n\n"
                for i, sent in enumerate(topic_sentences[:3], 1):  # Limit to 3 per section
                    # Clean sentence
                    sent = re.sub(r'^[•\-\*]+\s*', '', sent)
                    sent = re.sub(r'\s+([,.!?;:])', r'\1', sent)
                    if sent and sent[0].islower():
                        sent = sent[0].upper() + sent[1:]
                    structured_summary += f"• {sent}\n"
                structured_summary += "\n"
                section_num += 1

        # Add any remaining sentences as a general section
        if remaining_sentences:
            structured_summary += f"{section_num}. Additional Concepts\n\n"
            for sent in remaining_sentences[:3]:
                sent = re.sub(r'^[•\-\*]+\s*', '', sent)
                sent = re.sub(r'\s+([,.!?;:])', r'\1', sent)
                if sent and sent[0].islower():
                    sent = sent[0].upper() + sent[1:]
                structured_summary += f"• {sent}\n"

    return structured_summary.strip()

def generate_summary(text, sentences_count=3):
    """
    Generate a summary of the given text. Uses structured format for longer texts.

    Args:
        text (str): The text to summarize.
        sentences_count (int): Number of sentences in the summary (for fallback).

    Returns:
        str: The summarized text.
    """
    if not text.strip():
        return "No text available to summarize."

    # Use structured summary for texts longer than 1000 characters
    if len(text) > 1000:
        return generate_structured_summary(text)
    else:
        # Fallback to simple extractive summary for shorter texts
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary_sentences = summarizer(parser.document, sentences_count)

        sentences = [str(sentence).strip() for sentence in summary_sentences]
        cleaned_sentences = []
        for sentence in sentences:
            sentence = re.sub(r'^[•\-\*]+\s*', '', sentence)
            sentence = re.sub(r'\s+([,.!?;:])', r'\1', sentence)
            if sentence and sentence[0].islower():
                sentence = sentence[0].upper() + sentence[1:]
            cleaned_sentences.append(sentence)

        summary = '. '.join(cleaned_sentences)
        if summary and not summary.endswith('.'):
            summary += '.'
        return summary
