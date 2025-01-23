import streamlit as st
import requests
import google.generativeai as genai



# Configure Gemini API (Replace with your actual API key)
genai.configure(api_key=st.secrets("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def fetch_github_repos(username):
    """Fetch GitHub user's repositories."""
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def analyze_repositories(repos):
    """Analyze repository details."""
    repo_details = []
    for repo in repos:
        repo_details.append({
            'name': repo['name'],
            'language': repo.get('language', 'Unknown'),
            'description': repo.get('description', 'No description'),
            'stars': repo['stargazers_count']
        })
    return repo_details

def generate_roast(repo_details):
    """Generate roast using Gemini."""
    repo_summary = "\n".join([
        f"Repo: {r['name']}, Language: {r['language']}, Stars: {r['stars']}" 
        for r in repo_details
    ])
    
    prompt = f"""Generate a humorous roast based on this GitHub profile summary:
    {repo_summary}
    
    Roast the developer's coding skills, project choices, and GitHub activity with witty sarcasm.
    
    Do remember to keep it pretty short. Try to keep it under 3 paragraphs with 3 lines per paragraph. 
    
    Also, go HAM! Try to be really harsh so it actually makes someone want to start working harder and motivate them!!!
    
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title('🔥 GitHub Roast Generator')
    
    username = st.text_input('Enter GitHub Username')
    
    if st.button('Roast Me!'):
        with st.spinner('Fetching and analyzing repositories...'):
            repos = fetch_github_repos(username)
            
            if not repos:
                st.error('No repositories found or invalid username')
                return
            
            repo_details = analyze_repositories(repos)
            roast = generate_roast(repo_details)
            
            st.subheader('The Roast 🔥')
            st.write(roast)
            
            # Optional: Display repository summary
            with st.expander('Repository Details'):
                for repo in repo_details:
                    st.write(f"**{repo['name']}** - {repo['language']} ({repo['stars']} ⭐)")

if __name__ == '__main__':
    main()