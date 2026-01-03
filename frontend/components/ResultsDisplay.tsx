"use client";

import { CheckCircle2, XCircle, ExternalLink, AlertTriangle, TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface Citation {
  title: string;
  url: string;
}

interface ClaimResult {
  claim: string;
  status: "verified" | "hallucinated" | "error";
  confidence: number;
  similarity: number;
  credibility: number;
  contradicted: boolean;
  citations: Citation[];
  explanation: string;
}

interface ResultsDisplayProps {
  results: {
    domain: string;
    total_claims: number;
    overall_reliability: number;
    claims: ClaimResult[];
    extracted_citations?: {
      dois?: string[];
      urls?: string[];
    };
    citation_verification?: {
      verified: Array<{ url: string; title: string }>;
      invalid: Array<{ url: string; title: string; error?: string }>;
      total: number;
      verification_rate: number;
    };
  } | null;
  loading: boolean;
}

export function ResultsDisplay({ results, loading }: ResultsDisplayProps) {
  if (loading) {
    return (
      <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
        <CardContent className="p-6">
          <div className="flex items-center justify-center py-12">
            <div className="text-center space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-400 mx-auto"></div>
              <p className="text-cyan-400 font-medium">Analyzing claims...</p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!results) {
    return null;
  }

  // Show message if no claims found
  if (!results.claims || results.claims.length === 0) {
    return (
      <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
        <CardContent className="p-6">
          <div className="text-center py-8 space-y-2">
            <p className="text-gray-400 text-lg">No verifiable claims found</p>
            <p className="text-sm text-gray-500">
              The text may contain only opinions, questions, or conversational content.
            </p>
            <p className="text-xs text-gray-600 mt-4">
              Try providing factual statements, statistics, or claims that can be verified against web sources.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const verifiedCount = results.claims.filter((c) => c.status === "verified").length;
  const hallucinatedCount = results.claims.filter((c) => c.status === "hallucinated").length;

  return (
    <div className="space-y-6">
      {/* Overall Stats */}
      <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-2xl bg-gradient-to-r from-cyan-400 to-pink-500 bg-clip-text text-transparent">
            Verification Results
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Citation Verification Status */}
          {results.citation_verification && results.citation_verification.total > 0 && (
            <div className="p-4 bg-black/40 border border-cyan-500/30 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-400">Citation Verification</span>
                <span className="text-sm font-semibold text-cyan-400">
                  {Math.round(results.citation_verification.verification_rate * 100)}% Verified
                </span>
              </div>
              <div className="flex items-center gap-4 text-xs text-gray-500">
                <span>✓ {results.citation_verification.verified.length} Valid</span>
                <span>✗ {results.citation_verification.invalid.length} Invalid</span>
                <span>Total: {results.citation_verification.total}</span>
              </div>
            </div>
          )}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-black/40 border border-cyan-500/30 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="h-5 w-5 text-cyan-400" />
                <span className="text-sm text-gray-400">Overall Reliability</span>
              </div>
              <p className="text-3xl font-bold text-cyan-400">
                {(results.overall_reliability * 100).toFixed(0)}%
              </p>
            </div>
            <div className="p-4 bg-black/40 border border-green-500/30 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle2 className="h-5 w-5 text-green-400" />
                <span className="text-sm text-gray-400">Verified</span>
              </div>
              <p className="text-3xl font-bold text-green-400">{verifiedCount}</p>
            </div>
            <div className="p-4 bg-black/40 border border-red-500/30 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <XCircle className="h-5 w-5 text-red-400" />
                <span className="text-sm text-gray-400">Hallucinated</span>
              </div>
              <p className="text-3xl font-bold text-red-400">{hallucinatedCount}</p>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Domain Detected</span>
              <span className="text-cyan-400 font-semibold capitalize">{results.domain}</span>
            </div>
            <Progress 
              value={results.overall_reliability * 100} 
              className="h-2 bg-black/40"
            />
          </div>
        </CardContent>
      </Card>

      {/* Individual Claims */}
      <div className="space-y-4">
        <h3 className="text-xl font-semibold text-white">
          Claim Analysis ({results.total_claims} total)
        </h3>
        {results.claims.map((claim, index) => (
          <Card
            key={index}
            className={cn(
              "border backdrop-blur-sm transition-all duration-300",
              claim.status === "verified"
                ? "border-green-500/30 bg-green-500/5 hover:bg-green-500/10"
                : claim.status === "hallucinated"
                ? "border-red-500/30 bg-red-500/5 hover:bg-red-500/10"
                : "border-yellow-500/30 bg-yellow-500/5"
            )}
          >
            <CardContent className="p-6">
              <div className="space-y-4">
                {/* Claim Header */}
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      {claim.status === "verified" ? (
                        <CheckCircle2 className="h-5 w-5 text-green-400 flex-shrink-0" />
                      ) : claim.status === "hallucinated" ? (
                        <XCircle className="h-5 w-5 text-red-400 flex-shrink-0" />
                      ) : (
                        <AlertTriangle className="h-5 w-5 text-yellow-400 flex-shrink-0" />
                      )}
                      <span
                        className={cn(
                          "text-sm font-semibold px-3 py-1 rounded-full",
                          claim.status === "verified"
                            ? "bg-green-500/20 text-green-400"
                            : claim.status === "hallucinated"
                            ? "bg-red-500/20 text-red-400"
                            : "bg-yellow-500/20 text-yellow-400"
                        )}
                      >
                        {claim.status.toUpperCase()}
                      </span>
                      {claim.contradicted && (
                        <span className="text-xs text-yellow-400 bg-yellow-500/20 px-2 py-1 rounded-full">
                          Contradicted
                        </span>
                      )}
                    </div>
                    <p className="text-white text-lg leading-relaxed">{claim.claim}</p>
                  </div>
                </div>

                {/* Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-white/10">
                  <div>
                    <p className="text-xs text-gray-400 mb-1">Confidence</p>
                    <div className="flex items-center gap-2">
                      <Progress value={claim.confidence * 100} className="flex-1 h-2" />
                      <span className="text-sm font-semibold text-cyan-400">
                        {(claim.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400 mb-1">Similarity</p>
                    <div className="flex items-center gap-2">
                      <Progress value={claim.similarity * 100} className="flex-1 h-2" />
                      <span className="text-sm font-semibold text-purple-400">
                        {(claim.similarity * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400 mb-1">Credibility</p>
                    <div className="flex items-center gap-2">
                      <Progress value={claim.credibility * 100} className="flex-1 h-2" />
                      <span className="text-sm font-semibold text-pink-400">
                        {(claim.credibility * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Explanation */}
                {claim.explanation && (
                  <div className="pt-4 border-t border-white/10">
                    <p className="text-sm text-gray-400 mb-2">Explanation</p>
                    <p className="text-white/80 leading-relaxed">{claim.explanation}</p>
                  </div>
                )}

                {/* Citations */}
                {claim.citations && claim.citations.length > 0 && (
                  <div className="pt-4 border-t border-white/10">
                    <p className="text-sm text-gray-400 mb-3">Sources ({claim.citations.length})</p>
                    <div className="space-y-2">
                      {claim.citations.map((citation, idx) => (
                        <a
                          key={idx}
                          href={citation.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 p-3 bg-black/40 border border-cyan-500/20 rounded-lg hover:border-cyan-400/50 hover:bg-black/60 transition-all group"
                        >
                          <ExternalLink className="h-4 w-4 text-cyan-400 group-hover:text-cyan-300" />
                          <span className="text-sm text-cyan-300 group-hover:text-cyan-200 flex-1 truncate">
                            {citation.title || citation.url}
                          </span>
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

