"use client";

import { useState, useCallback, useRef } from "react";
import { FileText, Link, File, Upload, X, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type InputType = "text" | "url" | "file" | "batch";

interface InputAreaProps {
  onVerify: (type: InputType, data: any) => void;
  loading: boolean;
}

export function InputArea({ onVerify, loading }: InputAreaProps) {
  const [inputType, setInputType] = useState<InputType>("text");
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      if (droppedFile.type === "application/pdf" || droppedFile.name.endsWith(".pdf")) {
        setInputType("file");
        setFile(droppedFile);
      } else if (droppedFile.name.endsWith(".docx") || droppedFile.name.endsWith(".doc")) {
        setInputType("file");
        setFile(droppedFile);
      }
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setInputType("file");
    }
  };

  const handleVerify = () => {
    if (inputType === "text" && text.trim()) {
      onVerify("text", { text: text.trim() });
    } else if (inputType === "url" && url.trim()) {
      onVerify("url", { url: url.trim() });
    } else if (inputType === "file" && file) {
      onVerify("file", { file });
    }
  };

  const canVerify = 
    (inputType === "text" && text.trim()) ||
    (inputType === "url" && url.trim()) ||
    (inputType === "file" && file);

  return (
    <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
      <CardContent className="p-6">
        {/* Input Type Buttons */}
        <div className="flex gap-2 mb-6 flex-wrap">
          <Button
            variant={inputType === "text" ? "neon" : "ghost"}
            size="sm"
            onClick={() => {
              setInputType("text");
              setFile(null);
              setUrl("");
            }}
            className={cn(
              "transition-all duration-300",
              inputType === "text" && "shadow-[0_0_15px_rgba(34,211,238,0.5)]"
            )}
          >
            <FileText className="h-4 w-4" />
            Text
          </Button>
          <Button
            variant={inputType === "url" ? "neon" : "ghost"}
            size="sm"
            onClick={() => {
              setInputType("url");
              setFile(null);
              setText("");
            }}
            className={cn(
              "transition-all duration-300",
              inputType === "url" && "shadow-[0_0_15px_rgba(34,211,238,0.5)]"
            )}
          >
            <Link className="h-4 w-4" />
            URL
          </Button>
          <Button
            variant={inputType === "file" ? "neon" : "ghost"}
            size="sm"
            onClick={() => {
              setInputType("file");
              setText("");
              setUrl("");
              fileInputRef.current?.click();
            }}
            className={cn(
              "transition-all duration-300",
              inputType === "file" && "shadow-[0_0_15px_rgba(34,211,238,0.5)]"
            )}
          >
            <File className="h-4 w-4" />
            File
          </Button>
        </div>

        {/* Dynamic Input Area */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={cn(
            "relative border-2 border-dashed rounded-lg p-6 transition-all duration-300",
            isDragging
              ? "border-cyan-400 bg-cyan-500/10 shadow-[0_0_30px_rgba(34,211,238,0.3)]"
              : "border-cyan-500/30 bg-black/20",
            inputType === "file" && "min-h-[200px]"
          )}
        >
          {inputType === "text" && (
            <div className="space-y-4">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste or type your content here to verify claims..."
                className="w-full h-48 bg-black/40 border border-cyan-500/30 rounded-lg p-4 text-white placeholder:text-gray-500 focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 transition-all"
              />
            </div>
          )}

          {inputType === "url" && (
            <div className="space-y-4">
              <div className="flex gap-2">
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com/article"
                  className="flex-1 bg-black/40 border border-cyan-500/30 rounded-lg px-4 py-3 text-white placeholder:text-gray-500 focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 transition-all"
                />
              </div>
              <p className="text-sm text-gray-400">
                Enter a URL to extract and verify content from the webpage
              </p>
            </div>
          )}

          {inputType === "file" && (
            <div className="flex flex-col items-center justify-center space-y-4">
              {file ? (
                <div className="w-full space-y-4">
                  <div className="flex items-center justify-between p-4 bg-black/40 border border-cyan-500/30 rounded-lg">
                    <div className="flex items-center gap-3">
                      <File className="h-5 w-5 text-cyan-400" />
                      <div>
                        <p className="text-white font-medium">{file.name}</p>
                        <p className="text-sm text-gray-400">
                          {(file.size / 1024).toFixed(2)} KB
                        </p>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => setFile(null)}
                      className="text-red-400 hover:text-red-300"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ) : (
                <>
                  <Upload className="h-12 w-12 text-cyan-400/50" />
                  <div className="text-center">
                    <p className="text-white mb-2">
                      Drag and drop a file here, or{" "}
                      <button
                        onClick={() => fileInputRef.current?.click()}
                        className="text-cyan-400 hover:text-cyan-300 underline"
                      >
                        browse
                      </button>
                    </p>
                    <p className="text-sm text-gray-400">
                      Supports PDF and DOCX files
                    </p>
                  </div>
                </>
              )}
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={handleFileSelect}
                className="hidden"
              />
            </div>
          )}

          {isDragging && (
            <div className="absolute inset-0 flex items-center justify-center bg-cyan-500/10 rounded-lg border-2 border-cyan-400">
              <p className="text-cyan-400 font-semibold">Drop file here</p>
            </div>
          )}
        </div>

        {/* Verify Button */}
        <div className="mt-6">
          <Button
            onClick={handleVerify}
            disabled={!canVerify || loading}
            variant="neonPink"
            size="lg"
            className="w-full font-semibold text-lg py-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5 mr-2" />
                Verify Claims
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

