"""
Question Generator Agent

Generates categorized user questions based on product data.
Single responsibility: Question generation and categorization.
"""

from typing import Dict, Any, List
from agent_framework import BaseAgent, AgentResult, AgentStatus, agent_registry


class QuestionGeneratorAgent(BaseAgent):
    """
    Generates categorized user questions from product data.
    
    Input: Structured product data
    Output: Categorized question set
    """
    
    def __init__(self):
        super().__init__("QuestionGeneratorAgent")
        self.input_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "concentration": {"type": "string"},
                "skin_types": {"type": "array"},
                "key_ingredients": {"type": "array"},
                "benefits": {"type": "array"},
                "usage_instructions": {"type": "string"},
                "side_effects": {"type": "string"},
                "price": {"type": "string"}
            }
        }
        self.output_schema = {"type": "object"}
        
        # Question templates by category
        self.question_templates = {
            "Informational": [
                "What is {product_name}?",
                "What are the key ingredients in {product_name}?",
                "What concentration does {product_name} have?",
                "What are the main benefits of {product_name}?"
            ],
            "Safety": [
                "Are there any side effects of using {product_name}?",
                "Is {product_name} safe for sensitive skin?",
                "What precautions should I take when using {product_name}?",
                "Can {product_name} cause skin irritation?"
            ],
            "Usage": [
                "How do I use {product_name}?",
                "When should I apply {product_name}?",
                "How many drops of {product_name} should I use?",
                "Can I use {product_name} with other products?"
            ],
            "Skin Type": [
                "Is {product_name} suitable for oily skin?",
                "What skin types can use {product_name}?",
                "Will {product_name} work for combination skin?",
                "Is {product_name} good for sensitive skin?"
            ],
            "Purchase": [
                "What is the price of {product_name}?",
                "Where can I buy {product_name}?",
                "Is {product_name} worth the price?",
                "Does {product_name} come in different sizes?"
            ],
            "Comparison": [
                "How does {product_name} compare to other vitamin C serums?",
                "Is {product_name} better than similar products?",
                "What makes {product_name} different from competitors?",
                "Are there cheaper alternatives to {product_name}?"
            ],
            "Results": [
                "How long until I see results from {product_name}?",
                "Will {product_name} really fade dark spots?",
                "Can {product_name} brighten my skin?",
                "How effective is {product_name}?"
            ]
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input has basic product structure"""
        return "name" in input_data and isinstance(input_data["name"], str)
    
    def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Generate categorized questions from product data"""
        try:
            self.status = AgentStatus.RUNNING
            
            if not self.validate_input(input_data):
                return AgentResult(
                    agent_name=self.name,
                    status=AgentStatus.FAILED,
                    errors=["Invalid input data: missing product name"]
                )
            
            questions = []
            categories = set()
            
            # Generate questions from templates
            for category, templates in self.question_templates.items():
                for template in templates:
                    question = self._generate_question(template, input_data)
                    if question:
                        questions.append(question)
                        categories.add(category)
            
            # Generate specific questions based on available data
            specific_questions = self._generate_specific_questions(input_data)
            questions.extend(specific_questions)
            
            # Ensure minimum of 15 questions
            while len(questions) < 15:
                additional = self._generate_additional_questions(input_data, len(questions))
                questions.extend(additional)
            
            # Sort by priority and limit to reasonable number
            questions.sort(key=lambda q: q.get("priority", 1), reverse=True)
            questions = questions[:20]  # Keep top 20
            
            question_set = {
                "questions": questions,
                "categories": list(categories),
                "total_questions": len(questions),
            }
            
            self.status = AgentStatus.COMPLETED
            
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                data=question_set,
                metadata={
                    "categories": len(categories),
                    "questions_generated": len(questions)
                }
            )
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                errors=[f"Question generation failed: {str(e)}"]
            )
    
    def _generate_question(self, template: str, product_data: Dict[str, Any]) -> Dict[str, Any] | None:
        """Generate question from template"""
        try:
            question_text = template.format(
                product_name=product_data.get("name", "this product"),
                concentration=product_data.get("concentration", "this concentration"),
                price=product_data.get("price", "this price")
            )
            
            return {
                "question": question_text,
                "category": self._get_template_category(template),
                "priority": self._calculate_priority(template, product_data),
                "answerable": self._is_answerable(template, product_data),
            }
        except Exception:
            return None
    
    def _generate_specific_questions(self, product_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate questions specific to available product data"""
        questions = []
        
        # Skin type specific questions
        if product_data.get("skin_types"):
            for skin_type in product_data["skin_types"]:
                questions.append(
                    {
                        "question": f"Is {product_data['name']} good for {skin_type} skin?",
                        "category": "Skin Type",
                        "priority": 3,
                        "answerable": True,
                    }
                )
        
        # Ingredient specific questions
        if product_data.get("key_ingredients"):
            for ingredient in product_data["key_ingredients"][:2]:  # Limit to avoid too many
                questions.append(
                    {
                        "question": f"What are the benefits of {ingredient} in {product_data['name']}?",
                        "category": "Informational",
                        "priority": 2,
                        "answerable": True,
                    }
                )
        
        # Benefit specific questions
        if product_data.get("benefits"):
            for benefit in product_data["benefits"][:2]:
                questions.append(
                    {
                        "question": f"How does {product_data['name']} help with {benefit.lower()}?",
                        "category": "Results",
                        "priority": 3,
                        "answerable": True,
                    }
                )
        
        return questions
    
    def _generate_additional_questions(self, product_data: Dict[str, Any], current_count: int) -> List[Dict[str, Any]]:
        """Generate additional questions to meet minimum requirement"""
        additional_questions = []
        
        generic_templates = [
            ("Can I use {product_name} daily?", "Usage", 2),
            ("Should I use {product_name} in morning or night?", "Usage", 2),
            ("Is {product_name} suitable for beginners?", "Safety", 1),
            ("What makes {product_name} effective?", "Informational", 2),
            ("How long does one bottle of {product_name} last?", "Purchase", 1)
        ]
        
        for template, category, priority in generic_templates:
            if current_count + len(additional_questions) >= 15:
                break
                
            question = self._generate_question(template, product_data)
            if question:
                question["category"] = category
                question["priority"] = priority
                additional_questions.append(question)
        
        return additional_questions
    
    def _get_template_category(self, template: str) -> str:
        """Determine category from template content"""
        template_lower = template.lower()
        if "safe" in template_lower or "side effect" in template_lower or "precaution" in template_lower:
            return "Safety"
        elif "use" in template_lower or "apply" in template_lower or "how" in template_lower:
            return "Usage"
        elif "skin" in template_lower or "suitable" in template_lower:
            return "Skin Type"
        elif "price" in template_lower or "buy" in template_lower or "worth" in template_lower:
            return "Purchase"
        elif "compare" in template_lower or "different" in template_lower or "competitor" in template_lower:
            return "Comparison"
        elif "result" in template_lower or "effective" in template_lower or "work" in template_lower:
            return "Results"
        else:
            return "Informational"
    
    def _calculate_priority(self, template: str, product_data: Dict[str, Any]) -> int:
        """Calculate question priority based on importance"""
        template_lower = template.lower()
        
        # High priority questions
        if any(keyword in template_lower for keyword in ["how to use", "side effects", "price"]):
            return 5
        elif any(keyword in template_lower for keyword in ["what is", "benefits", "suitable"]):
            return 4
        elif any(keyword in template_lower for keyword in ["ingredients", "concentration"]):
            return 3
        elif any(keyword in template_lower for keyword in ["compare", "different"]):
            return 2
        else:
            return 1
    
    def _is_answerable(self, template: str, product_data: Dict[str, Any]) -> bool:
        """Check if question can be answered from available data"""
        template_lower = template.lower()
        
        # Questions about external comparisons or purchasing locations can't be answered
        if any(keyword in template_lower for keyword in ["where to buy", "compare to other", "competitors"]):
            return False
        
        return True


# Register the agent
agent_registry.register(QuestionGeneratorAgent())
