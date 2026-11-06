# Project Report: M1-P2

## AI-Powered Meeting-to-Action Assistant

**Student name:** Nitin Naik 
**USN:** 1CR25AI406  
**Department:** AIML  
**Subject / course code:** Agentic AI 
**Submission date:** 06 November 2026

## 1\. Abstract

The Meeting-to-Action Assistant is a local web-based prototype that converts meeting notes into structured information. It uses sentence splitting and text-pattern rules to identify likely decisions, action items, owners, deadline phrases, unresolved issues, and clarification questions. The application displays the extracted information and allows action items to be downloaded as a CSV file. The current implementation uses Python and Streamlit and does not require a paid AI API.

## 2\. Problem Statement

Meeting notes can contain decisions and tasks mixed with general discussion. It may be difficult to identify who must do what and by when. This project helps organize likely action items and highlights missing ownership or deadlines for human review.

## 3\. Objectives

* Accept meeting notes or a transcript as text.
* Produce a concise extractive summary.
* Identify explicit decision phrases.
* Extract likely tasks, owners, and deadline phrases.
* Detect explicit unresolved phrases.
* Generate clarification questions when owner or deadline information is missing.
* Export extracted action items to CSV.

## 4\. Existing System

Meeting participants often review notes manually and create separate task lists. Important assignments or missing details may be overlooked.

## 5\. Proposed System

The proposed prototype provides a single interface for entering notes and viewing a summary, decisions, action items, unresolved items, and clarification questions.

## 6\. System Requirements

**Software:** Python 3.11/3.12, Streamlit, Pandas, web browser, Windows.  
**Hardware:** A laptop/desktop capable of running Python. Internet is needed to install packages but not for normal local use afterward.

## 7\. Methodology / Algorithm

1. Accept transcript text.
2. Split it into sentences.
3. Detect decision phrases using a predefined keyword list.
4. Search for common assignment patterns, such as a person's name followed by “will”.
5. Detect common task verbs and deadline phrases.
6. Flag sentences containing phrases such as “not finalized” or “pending”.
7. Create clarification questions for likely tasks with missing owners or deadlines.
8. Display the output and provide a CSV download.

## 8\. Architecture

Meeting notes → Streamlit interface → Sentence processing and rule-based extraction → Summary / decisions / tasks / unresolved items → CSV export.

## 9\. Testing

Record your actual test results after running the app.

|Test|Input|Expected result|Actual result|
|-|-|-|-|
|T1|“Rahul will prepare the slides by Thursday.”|Owner Rahul, task prepare slides, deadline Thursday|Passed – Owner Rahul, task and Thursday deadline extracted correctly|
|T2|“The venue is not finalized.”|Sentence listed as unresolved|Passed – Unresolved sentence displayed correctly|
|T3|Empty input|Validation message displayed|Passed – Validation message displayed for empty input|
|T4|Task without an owner or deadline|Clarification question may be generated|Passed – Clarification question generated for missing owner or deadline|

## 10\. Results and Discussion

Insert screenshots of the input area, meeting summary, decisions, action-items table, clarification questions, and CSV download. Explain any extraction errors you observed.

## 11\. Limitations

The current version is rule-based rather than a true language-model assistant. It may miss tasks expressed in unusual wording, mistake some sentences for tasks, and cannot reliably understand complex context. Deadline phrases are not converted to calendar dates. Always verify results against the original notes.

## 12\. Future Enhancements

* Add a local open-source language model for semantic extraction.
* Support uploaded transcript files and speech-to-text.
* Improve owner and deadline detection.
* Add editable tasks, status tracking, and persistent storage.
* Evaluate precision and recall on a labelled meeting-note dataset.

## 13\. Conclusion

The project demonstrates a basic workflow for converting unstructured meeting notes into a structured action list and highlighting incomplete information for human follow-up.

## 14\. References

* Python documentation: https://docs.python.org/3/
* Streamlit documentation: https://docs.streamlit.io/
* Pandas documentation: https://pandas.pydata.org/docs/

**Before submission:** replace placeholders, add your own screenshots, and record real test results. Do not claim features that you have not implemented.

