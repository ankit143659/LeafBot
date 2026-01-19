
// Fix: Use strictly the recommended import for GoogleGenAI
import { GoogleGenAI } from "@google/genai";

export interface MediaPart {
  inlineData: {
    mimeType: string;
    data: string;
  };
}

export const generateAIResponse = async (
  prompt: string, 
  history: { role: string; parts: ( { text: string } | MediaPart )[] }[],
  image?: { mimeType: string; data: string }
): Promise<string> => {
  // Fix: Initialize GoogleGenAI inside the function as recommended
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
  
  try {
    const contents: any[] = [...history];
    const currentParts: any[] = [{ text: prompt }];

    if (image) {
      currentParts.push({
        inlineData: {
          mimeType: image.mimeType,
          data: image.data,
        }
      });
    }

    contents.push({ role: 'user', parts: currentParts });

    // Fix: Using 'gemini-3-pro-preview' for complex reasoning/STEM tasks as per guidelines
    const response = await ai.models.generateContent({
      model: 'gemini-3-fllash-preview',
      contents: contents,
      config: {
        systemInstruction: `Your name is "FloraExpert". You are a friendly and professional plant health assistant for farmers and botanical enthusiasts.

        RULES FOR RESPONSE:
        1. LANGUAGE: Use simple, professional English. Do not use Hindi or slang.
        2. STRUCTURE: Use clear bullet points and emojis.
           - ## 🌱 Plant Identification
           - ## 🏥 Diagnosis (What's wrong?)
           - ## 🛠️ Care Plan (Step-by-step actions)
           - ## 💧 Vital Stats (Light, Water, Soil - use simple table)
        3. TONE: Helpful, encouraging, and clear.
        4. IMAGES: If an image is provided, analyze the leaves, stem, and soil carefully.
        5. AUTOMATION: Mention that the user can set up automated email alerts for regular health updates on this specific plant.

        Goal: Ensure even a regular gardener can easily understand and take action to save their plant.`,
        temperature: 0.6,
        topP: 0.9,
      }
    });

    // Fix: Use response.text property directly
    return response.text || "I'm sorry, I couldn't process that report. Please try again.";
  } catch (error) {
    console.error("Gemini API Error:", error);
    return "Error: System is currently busy. Please try again in a few moments.";
  }
};
