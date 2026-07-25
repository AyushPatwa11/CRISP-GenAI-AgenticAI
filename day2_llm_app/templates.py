from langchain_core.prompts import PromptTemplate

RESUME_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["resume_text", "job_description", "target_role"],
    template="""You are an expert HR Executive and Technical Recruiter.
Analyze the following Candidate Resume against the Target Job Description for the role of '{target_role}'.

--- RESUME CONTENT ---
{resume_text}

--- TARGET JOB DESCRIPTION ---
{job_description}

Provide a structured assessment in valid JSON format matching this schema EXACTLY:
{{
  "match_score": 85,
  "summary": "Brief 2-sentence executive summary of fit.",
  "matching_skills": ["Skill 1", "Skill 2"],
  "missing_skills": ["Missing Skill 1", "Missing Skill 2"],
  "key_strengths": ["Strength 1", "Strength 2"],
  "improvement_recommendations": ["Recommendation 1", "Recommendation 2"],
  "tailored_cover_letter": "A compelling 3-paragraph cover letter tailored to the job description."
}}

Ensure response is raw valid JSON without markdown wrapping.
"""
)
