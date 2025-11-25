from flask import Flask, request, jsonify 
import os                                                                     
from groq import Groq
from dotenv import load_dotenv   

load_dotenv()
app= Flask(__name__)
groq_client= Groq(api_key=os.getenv("GROQ_API_KEY"))
SYSTEM_PROMPT = (
    "You are a magical, extremely dramatic fortune teller. "
    "Your prophecies are funny, exaggerated, mystical, and full of nonsense. "
    "You must ALWAYS answer with humor, even if the user's question is serious."
)

#Implementing a /fortune endpoint:
@app.route("/fortune", methods=["POST"])
def fortune():
    try:   
        data=request.get_json()
        #Invalid JSON request
        if data is None:
            return jsonify({"error": "Invalid JSON request"}), 400
        
        #Accepting the user’s name and/or a question:
        name= data.get("name")
        question= data.get("question")

        #Empty strings
        if isinstance(name, str):
            name = name.strip()
        else:
            name = None
        
        if isinstance(question, str):
            question = question.strip()
        else:
            question = None
            
        #Missing name/question :
        if not name and not question:
            return jsonify({"error": "Please provide one name or question"}), 400
        
        content = ""   
        if name:
            content += f"Nom : {name}. "
        if question:
            content += f"Question : {question}. "

            # Call Groq and return the prophecy”
        response = groq_client.chat.completions.create(
            model="groq/compound", 
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ],
            temperature=0.8, 
            max_completion_tokens=200  
        )
        prophecy = response.choices[0].message.content  
        result = {
            "name": name if name else "None",
            "question": question if question else "No question",
            "prophecy": prophecy
        }
        return jsonify(result)      
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)