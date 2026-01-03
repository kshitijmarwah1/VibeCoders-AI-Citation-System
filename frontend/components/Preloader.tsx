"use client";

import { useEffect, useState, useRef } from "react";
import { Brain, Sparkles } from "lucide-react";

export function Preloader() {
  const [isLoading, setIsLoading] = useState(true);
  const [isFading, setIsFading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [particles, setParticles] = useState<Array<{ left: number; top: number; delay: number; duration: number }>>([]);
  const startTimeRef = useRef<number>(Date.now());
  const pageLoadedRef = useRef<boolean>(false);
  const fadeTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Generate particle positions only on client
    setParticles(
      Array.from({ length: 12 }, () => ({
        left: Math.random() * 100,
        top: Math.random() * 100,
        delay: Math.random() * 2,
        duration: 2 + Math.random() * 2,
      }))
    );

    // Simulate loading progress
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        return prev + Math.random() * 15;
      });
    }, 100);

    // Function to handle fade-out with minimum time guarantee
    const handleFadeOut = () => {
      if (fadeTimeoutRef.current) return; // Already scheduled
      
      const elapsed = Date.now() - startTimeRef.current;
      const minimumTime = 1500; // 1.5 seconds
      const remainingTime = Math.max(0, minimumTime - elapsed);
      const fadeDuration = 800; // 800ms fade-out duration

      fadeTimeoutRef.current = setTimeout(() => {
        setProgress(100);
        setIsFading(true);
        
        // Remove from DOM after fade completes
        setTimeout(() => {
          setIsLoading(false);
        }, fadeDuration);
      }, remainingTime);
    };

    // Check if page is fully loaded
    const handleLoad = () => {
      if (!pageLoadedRef.current) {
        pageLoadedRef.current = true;
        handleFadeOut();
      }
    };

    // If page is already loaded
    if (document.readyState === "complete") {
      handleLoad();
    } else {
      window.addEventListener("load", handleLoad);
    }

    return () => {
      clearInterval(progressInterval);
      window.removeEventListener("load", handleLoad);
      if (fadeTimeoutRef.current) {
        clearTimeout(fadeTimeoutRef.current);
      }
    };
  }, []);

  if (!isLoading) return null;

  return (
    <div
      className={`fixed inset-0 z-[9999] flex items-center justify-center bg-black transition-opacity duration-800 ease-in-out ${
        isFading ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
    >
      {/* Animated background gradient */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/3 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-2000"></div>
      </div>

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center justify-center space-y-8">
        {/* Logo with animations */}
        <div className="relative">
          {/* Outer rotating ring */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-32 h-32 border-2 border-cyan-400/30 rounded-full animate-spin-slow">
              <div className="absolute top-0 left-1/2 w-1 h-1 bg-cyan-400 rounded-full transform -translate-x-1/2"></div>
              <div className="absolute bottom-0 left-1/2 w-1 h-1 bg-pink-400 rounded-full transform -translate-x-1/2"></div>
              <div className="absolute left-0 top-1/2 w-1 h-1 bg-purple-400 rounded-full transform -translate-y-1/2"></div>
              <div className="absolute right-0 top-1/2 w-1 h-1 bg-cyan-400 rounded-full transform -translate-y-1/2"></div>
            </div>
          </div>

          {/* Middle pulsing ring */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-24 h-24 border border-pink-400/20 rounded-full animate-ping"></div>
          </div>

          {/* Brain icon with gradient */}
          <div className="relative flex items-center justify-center">
            <Brain className="h-16 w-16 text-cyan-400 animate-pulse" />
            <Sparkles className="h-6 w-6 text-pink-500 absolute -top-1 -right-1 animate-spin" />
            <Sparkles className="h-4 w-4 text-purple-500 absolute -bottom-1 -left-1 animate-pulse delay-1000" />
          </div>

          {/* Glowing effect */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-20 h-20 bg-cyan-400/10 rounded-full blur-xl animate-pulse"></div>
          </div>
        </div>

        {/* Text */}
        <div className="text-center space-y-2">
          <h2 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-pink-500 to-purple-500 bg-clip-text text-transparent animate-pulse">
            VibeVerifier
          </h2>
          <p className="text-sm text-gray-400">Loading your verification system...</p>
        </div>

        {/* Progress bar */}
        <div className="w-64 space-y-2">
          <div className="w-full bg-black/60 rounded-full h-1.5 overflow-hidden border border-cyan-500/20">
            <div
              className="h-full bg-gradient-to-r from-cyan-400 via-pink-500 to-purple-500 transition-all duration-300 ease-out relative"
              style={{ width: `${Math.min(progress, 100)}%` }}
            >
              <div className="absolute inset-0 bg-white/20 animate-shimmer"></div>
            </div>
          </div>
          <div className="text-center">
            <span className="text-xs text-cyan-400 font-medium">
              {Math.round(Math.min(progress, 100))}%
            </span>
          </div>
        </div>

        {/* Floating particles */}
        <div className="absolute inset-0 pointer-events-none">
          {particles.map((particle, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 rounded-full bg-cyan-400/40 animate-float"
              style={{
                left: `${particle.left}%`,
                top: `${particle.top}%`,
                animationDelay: `${particle.delay}s`,
                animationDuration: `${particle.duration}s`,
              }}
            ></div>
          ))}
        </div>
      </div>
    </div>
  );
}

