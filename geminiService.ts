
import { GoogleGenAI } from "@google/genai";
import { MenuItem } from "../types";

export const getChefRecommendation = async (userPrompt: string, menu: MenuItem[]) => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
  const menuSummary = menu.map(m => `${m.name} (${m.price} FCFA): ${m.description}`).join('\n');

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: `Tu es le Chef de Teranga Gourmet. Voici notre menu :\n${menuSummary}\n\nL'utilisateur demande : "${userPrompt}". Réponds de manière chaleureuse, courte et suggère un ou deux plats spécifiques.`,
      config: {
        thinkingConfig: { thinkingBudget: 0 }
      }
    });
    return response.text || "Désolé, je suis occupé en cuisine. Que puis-je vous servir ?";
  } catch (error) {
    console.error("AI Error:", error);
    return "Je vous suggère notre fameux Thieboudienne !";
  }
};
