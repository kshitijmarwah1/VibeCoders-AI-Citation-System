"use client";

import { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { AnimatedGradient } from "@/components/AnimatedGradient";
import { InputArea } from "@/components/InputArea";
import { ResultsDisplay } from "@/components/ResultsDisplay";
import { DynamicProgressBar } from "@/components/DynamicProgressBar";

// Get API base URL function - call at runtime to ensure env vars are available
const getApiBaseUrl = () => {
  // Always use absolute URL - never relative
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  
  // Validate and return environment URL if valid
  if (envUrl && typeof envUrl === 'string' && (envUrl.startsWith('http://') || envUrl.startsWith('https://'))) {
    // Remove trailing slash if present
    const url = envUrl.replace(/\/$/, '');
    console.log('[API Config] Using environment URL:', url);
    return url;
  }
  
  // Default to backend server - MUST be absolute URL
  const defaultUrl = "http://127.0.0.1:8000";
  console.log('[API Config] Using default URL:', defaultUrl);
  console.log('[API Config] NEXT_PUBLIC_API_URL was:', envUrl);
  return defaultUrl;
};

export default function Home() {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<{ percentage: number; message: string } | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);

  const handleVerify = async (type: string, data: any) => {
    setLoading(true);
    setError(null);
    setResults(null);
    setProgress({ percentage: 0, message: "Initializing..." });
    setTaskId(null);

    try {
      let response;
      const formData = new FormData();

      if (type === "text") {
        setProgress({ percentage: 0, message: "Starting verification..." });
        
        const baseUrl = getApiBaseUrl();
        // Ensure URL is absolute
        if (!baseUrl || (!baseUrl.startsWith('http://') && !baseUrl.startsWith('https://'))) {
          throw new Error(`Invalid API URL: ${baseUrl}. Must be an absolute URL starting with http:// or https://`);
        }
        const apiUrl = `${baseUrl}/verify/text`;
        console.log("API Base URL:", baseUrl);
        console.log("Making request to:", apiUrl);
        
        response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text: data.text }),
        });
      } else if (type === "url") {
        setProgress({ percentage: 0, message: "Fetching URL content..." });
        
        const baseUrl = getApiBaseUrl();
        const apiUrl = `${baseUrl}/verify/url`;
        console.log("API Base URL:", baseUrl);
        console.log("Making request to:", apiUrl);
        
        response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ url: data.url }),
        });
      } else if (type === "file") {
        formData.append("file", data.file);
        setProgress({ percentage: 5, message: "Uploading file..." });
        
        const baseUrl = getApiBaseUrl();
        const apiUrl = `${baseUrl}/verify/file`;
        console.log("API Base URL:", baseUrl);
        console.log("Making request to:", apiUrl);
        
        response = await fetch(apiUrl, {
          method: "POST",
          body: formData,
        });
      }

      if (!response || !response.ok) {
        const errorText = response ? await response.text() : "No response from server";
        console.error("Error response:", errorText);
        throw new Error(`HTTP error! status: ${response?.status || 'unknown'} - ${errorText}`);
      }

      // Read response
      const resultData = await response.json();
      
      // Validate response structure
      if (!resultData) {
        throw new Error("Empty response from server");
      }
      
      // Use backend task_id for progress tracking
      if (resultData.task_id) {
        setTaskId(resultData.task_id);
      }
      
      // Ensure results have the expected structure (remove task_id from display)
      const { task_id: _, ...restData } = resultData;
      const validatedResults = {
        domain: restData.domain || "general",
        total_claims: restData.total_claims || (restData.claims ? restData.claims.length : 0),
        overall_reliability: restData.overall_reliability || 0.0,
        claims: restData.claims || [],
        extracted_citations: restData.extracted_citations || {},
        citation_verification: restData.citation_verification || { verified: [], invalid: [], total: 0 }
      };
      
      // Show results - progress bar will continue updating until completion
      setProgress(null);
      setResults(validatedResults);
      
      // Keep loading state until progress shows completion
      // Progress bar will handle setting loading to false when done
    } catch (err) {
      console.error("Verification error:", err);
      setError(err instanceof Error ? err.message : "Failed to verify content. Please try again.");
      setProgress(null);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      <AnimatedGradient />
      <Navbar />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Hero Section */}
          <div className="text-center space-y-4 mb-12">
            <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-cyan-400 via-pink-500 to-purple-500 bg-clip-text text-transparent">
              AI Hallucination Detector
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Verify factual claims, detect hallucinations, and get confidence scores with 
              <span className="text-cyan-400 font-semibold"> real-time web verification</span>
            </p>
          </div>

          {/* Input Area */}
          <InputArea onVerify={handleVerify} loading={loading} />

          {/* Dynamic Progress Bar */}
          {taskId && (
            <DynamicProgressBar 
              taskId={taskId} 
              onComplete={() => {
                setTaskId(null);
                setProgress(null);
                setLoading(false);
              }} 
            />
          )}
          
          {/* Progress Display (fallback) */}
          {progress && !taskId && (
            <div className="p-6 bg-black/40 border border-cyan-500/30 rounded-lg backdrop-blur-sm">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-cyan-400 font-medium">{progress.message}</span>
                  <span className="text-cyan-400 font-semibold">{Math.round(progress.percentage)}%</span>
                </div>
                <div className="w-full bg-black/60 rounded-full h-2 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-cyan-400 via-pink-500 to-purple-500 transition-all duration-300 ease-out"
                    style={{ width: `${progress.percentage}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
              <p className="text-red-400">{error}</p>
            </div>
          )}

          {/* Results */}
          {results && (
            <div>
              <ResultsDisplay results={results} loading={false} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
