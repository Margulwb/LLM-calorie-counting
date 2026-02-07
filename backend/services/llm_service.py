"""
LLM Service for interacting with Ollama and RAG system
"""
import os
from typing import Dict, List, Optional
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


class LLMService:
    
    def __init__(self):
        self.model_name = os.getenv('OLLAMA_MODEL', 'mistral')
        self.knowledge_base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'knowledge_base'
        )
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # Initialize or load vector store
        self.vector_store = self._initialize_vector_store()
        
    def _initialize_vector_store(self):
        """Initialize or load the vector store with knowledge base"""
        persist_directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'chroma_db'
        )
        
        # Try to load existing vector store
        if os.path.exists(persist_directory):
            try:
                return Chroma(
                    persist_directory=persist_directory,
                    embedding_function=self.embeddings
                )
            except:
                pass
        
        # Create new vector store
        documents = self._load_knowledge_base()
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )
        
        return vector_store
    
    def _load_knowledge_base(self) -> List[Document]:
        """Load all markdown files from knowledge base"""
        documents = []
        
        if not os.path.exists(self.knowledge_base_path):
            print(f"Warning: Knowledge base path not found: {self.knowledge_base_path}")
            return documents
        
        for filename in os.listdir(self.knowledge_base_path):
            if filename.endswith('.md'):
                file_path = os.path.join(self.knowledge_base_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Split into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                
                chunks = text_splitter.split_text(content)
                
                for chunk in chunks:
                    documents.append(Document(
                        page_content=chunk,
                        metadata={'source': filename}
                    ))
        
        return documents
    
    def _get_relevant_context(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context from vector store"""
        docs = self.vector_store.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API"""
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return f"Przepraszam, wystąpił błąd podczas przetwarzania zapytania. Upewnij się, że Ollama jest uruchomiona i model {self.model_name} jest zainstalowany."
    
    def ask_expert(self, question: str, context: Optional[Dict] = None) -> str:
        """
        Ask the diet expert a question
        
        Args:
            question: User's question
            context: Optional user context (weight, height, etc.)
            
        Returns:
            Expert's answer
        """
        # Get relevant knowledge from RAG
        relevant_knowledge = self._get_relevant_context(question, k=3)
        
        # Build context string
        context_str = ""
        if context:
            context_str = "\n\nInformacje o użytkowniku:\n"
            if 'weight' in context:
                context_str += f"- Waga: {context['weight']} kg\n"
            if 'height' in context:
                context_str += f"- Wzrost: {context['height']} cm\n"
            if 'age' in context:
                context_str += f"- Wiek: {context['age']} lat\n"
            if 'gender' in context:
                context_str += f"- Płeć: {context['gender']}\n"
            if 'activity_level' in context:
                context_str += f"- Poziom aktywności: {context['activity_level']}\n"
        
        # Create prompt
        prompt = f"""Jesteś ekspertem od odchudzania, diety i treningów. Odpowiadaj po polsku, profesjonalnie ale przystępnie.

Baza wiedzy:
{relevant_knowledge}
{context_str}

Pytanie użytkownika: {question}

Odpowiedz konkretnie, praktycznie i z przykładami. Jeśli pytanie dotyczy obliczeń, podaj konkretne liczby. Jeśli dotyczy planów, przedstaw szczegółowy plan działania."""

        return self._call_ollama(prompt)
    
    def generate_meal_plan(self, data: Dict) -> str:
        """Generate personalized meal plan"""
        calories = data['calories']
        protein = data.get('protein', calories * 0.3 / 4)
        carbs = data.get('carbs', calories * 0.4 / 4)
        fats = data.get('fats', calories * 0.3 / 9)
        meals = data.get('meals', 3)
        preferences = data.get('preferences', [])
        restrictions = data.get('restrictions', [])
        
        # Get relevant nutrition knowledge
        relevant_knowledge = self._get_relevant_context("planowanie posiłków makroskładniki", k=2)
        
        prompt = f"""Jesteś dietetykiem specjalizującym się w odchudzaniu. Stwórz szczegółowy plan posiłków na jeden dzień.

Wymagania:
- Kalorie dziennie: {calories} kcal
- Białko: {protein}g
- Węglowodany: {carbs}g
- Tłuszcze: {fats}g
- Liczba posiłków: {meals}

{f"Preferencje: {', '.join(preferences)}" if preferences else ""}
{f"Ograniczenia/Alergie: {', '.join(restrictions)}" if restrictions else ""}

Baza wiedzy:
{relevant_knowledge}

Stwórz konkretny plan zawierający:
1. Dokładne posiłki z wagą składników
2. Przybliżone kalorie i makro dla każdego posiłku
3. Prosty przepis/instrukcję dla każdego posiłku
4. Suma końcowa pasująca do założeń

Format: dla każdego posiłku podaj nazwę, składniki z wagą, sposób przygotowania, wartości odżywcze."""

        return self._call_ollama(prompt)
    
    def generate_workout_plan(self, data: Dict) -> str:
        """Generate workout plan"""
        goal = data['goal']
        experience = data.get('experience', 'beginner')
        days = data.get('days_per_week', 3)
        duration = data.get('duration', 60)
        workout_type = data.get('type', 'both')
        
        # Get relevant workout knowledge
        relevant_knowledge = self._get_relevant_context("trening siłowy cardio plan treningowy", k=3)
        
        prompt = f"""Jesteś trenerem personalnym specjalizującym się w odchudzaniu i budowie sylwetki. Stwórz szczegółowy plan treningowy.

Parametry:
- Cel: {goal}
- Poziom zaawansowania: {experience}
- Liczba dni treningowych w tygodniu: {days}
- Czas trwania sesji: {duration} minut
- Typ treningu: {workout_type}

Baza wiedzy:
{relevant_knowledge}

Stwórz kompletny plan treningowy zawierający:
1. Podział treningów na dni tygodnia
2. Szczegółowe ćwiczenia z liczbą serii i powtórzeń
3. Czas odpoczynku między seriami
4. Wskazówki techniczne dla początkujących
5. Progresja (jak zwiększać obciążenie/intensywność)
6. Rozgrzewka i rozciąganie

Dostosuj plan do poziomu zaawansowania i celu."""

        return self._call_ollama(prompt)
    
    def analyze_progress(self, data: Dict) -> str:
        """Analyze user's progress and provide recommendations"""
        current = data['current_weight']
        starting = data['starting_weight']
        weeks = data['weeks_elapsed']
        goal = data.get('goal_weight')
        issue = data.get('issue', '')
        
        weight_lost = starting - current
        weekly_rate = weight_lost / weeks if weeks > 0 else 0
        
        # Get relevant knowledge about progress and plateaus
        relevant_knowledge = self._get_relevant_context("plateau waga stoi postępy redukcja", k=3)
        
        prompt = f"""Jesteś ekspertem od analizy postępów w odchudzaniu. Przeanalizuj sytuację użytkownika i dorадź co robić.

Dane użytkownika:
- Waga początkowa: {starting} kg
- Waga aktualna: {current} kg
- Stracone: {weight_lost} kg
- Czas trwania: {weeks} tygodni
- Tempo: {weekly_rate:.2f} kg/tydzień
{f"- Waga docelowa: {goal} kg" if goal else ""}
{f"- Problem: {issue}" if issue else ""}

Baza wiedzy:
{relevant_knowledge}

Przeprowadź szczegółową analizę:
1. Oceń tempo redukcji (czy optymalne?)
2. Zidentyfikuj potencjalne problemy
3. Podaj konkretne rozwiązania:
   - Co zmienić w diecie (czy zmniejszyć kalorie?)
   - Co zmienić w treningu
   - Jak radzić sobie psychicznie
4. Realny plan na najbliższe tygodnie
5. Kiedy spodziewać się efektów

Bądź konstruktywny, motywujący ale realistyczny."""

        return self._call_ollama(prompt)
