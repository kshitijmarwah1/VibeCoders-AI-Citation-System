"use client";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/Navbar";
import { AnimatedGradient } from "@/components/AnimatedGradient";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Book, Code, Shield, Users, Github, ExternalLink, User } from "lucide-react";
import Link from "next/link";

interface GitHubUser {
  login: string;
  name: string | null;
  avatar_url: string;
  bio: string | null;
  html_url: string;
  location: string | null;
  public_repos: number;
  followers: number;
  following: number;
}

const GITHUB_REPO_URL = "https://github.com/kshitijmarwah1/VibeCoders-AI-Citation-System";
const CONTRIBUTORS = [
  { username: "BeastBoom", name: "Dhruv Gupta", url: "https://github.com/BeastBoom" },
  { username: "kshitijmarwah1", name: "Kshitij Marwah", url: "https://github.com/kshitijmarwah1" }
];

export default function DocsPage() {
  const [contributors, setContributors] = useState<(GitHubUser & { displayName: string })[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContributors = async () => {
      try {
        const users = await Promise.all(
          CONTRIBUTORS.map(async (contributor) => {
            const response = await fetch(`https://api.github.com/users/${contributor.username}`);
            if (response.ok) {
              const data = await response.json();
              return {
                ...data,
                displayName: contributor.name
              };
            }
            return null;
          })
        );
        setContributors(users.filter(Boolean) as (GitHubUser & { displayName: string })[]);
      } catch (error) {
        console.error("Error fetching GitHub users:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchContributors();
  }, []);
  return (
    <div className="min-h-screen relative overflow-hidden">
      <AnimatedGradient />
      <Navbar />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Header */}
          <div className="text-center space-y-4 mb-12">
            <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-cyan-400 via-pink-500 to-purple-500 bg-clip-text text-transparent">
              Documentation
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Complete guide to VibeVerifier - Setup, API, Privacy, and more
            </p>
          </div>

          {/* Navigation Tabs */}
          <Tabs defaultValue="setup" className="w-full">
            <TabsList className="grid w-full grid-cols-6 bg-black/40 border border-cyan-500/30">
              <TabsTrigger value="setup" className="flex items-center gap-2">
                <Book className="h-4 w-4" />
                Setup
              </TabsTrigger>
              <TabsTrigger value="api" className="flex items-center gap-2">
                <Code className="h-4 w-4" />
                API
              </TabsTrigger>
              <TabsTrigger value="privacy" className="flex items-center gap-2">
                <Shield className="h-4 w-4" />
                Privacy
              </TabsTrigger>
              <TabsTrigger value="credits" className="flex items-center gap-2">
                <Users className="h-4 w-4" />
                Credits
              </TabsTrigger>
              <TabsTrigger value="team" className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Team
              </TabsTrigger>
              <TabsTrigger value="github" className="flex items-center gap-2">
                <Github className="h-4 w-4" />
                GitHub
              </TabsTrigger>
            </TabsList>

            {/* Setup Tab */}
            <TabsContent value="setup" className="space-y-6">
              <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-cyan-400">Installation Guide</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6 text-gray-300">
                  <Section title="Prerequisites">
                    <ul className="list-disc list-inside space-y-2 ml-4">
                      <li>Python 3.9 or higher</li>
                      <li>Node.js 18.0 or higher</li>
                      <li>npm, yarn, or pnpm</li>
                      <li>Tavily API Key (<a href="https://tavily.com" target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:underline">Get one here</a>)</li>
                    </ul>
                  </Section>

                  <Section title="Backend Setup">
                    <div className="space-y-4">
                      <Step number="1" title="Navigate to backend directory">
                        <code className="block bg-black/60 p-2 rounded mt-2">cd backend</code>
                      </Step>
                      <Step number="2" title="Create virtual environment">
                        <div className="space-y-2 mt-2">
                          <code className="block bg-black/60 p-2 rounded">python -m venv venv</code>
                          <p className="text-sm text-gray-400">Windows: <code className="text-cyan-400">venv\Scripts\activate</code></p>
                          <p className="text-sm text-gray-400">macOS/Linux: <code className="text-cyan-400">source venv/bin/activate</code></p>
                        </div>
                      </Step>
                      <Step number="3" title="Install dependencies">
                        <code className="block bg-black/60 p-2 rounded mt-2">pip install -r requirements.txt</code>
                      </Step>
                      <Step number="4" title="Configure environment variables">
                        <p className="text-sm text-gray-400 mt-2">Create a <code className="text-cyan-400">.env</code> file in the backend directory:</p>
                        <code className="block bg-black/60 p-2 rounded mt-2">TAVILY_API_KEY=your_tavily_api_key_here</code>
                      </Step>
                      <Step number="5" title="Start the backend server">
                        <code className="block bg-black/60 p-2 rounded mt-2">uvicorn services.api.main:app --reload --port 8000</code>
                      </Step>
                    </div>
                  </Section>

                  <Section title="Frontend Setup">
                    <div className="space-y-4">
                      <Step number="1" title="Navigate to frontend directory">
                        <code className="block bg-black/60 p-2 rounded mt-2">cd frontend</code>
                      </Step>
                      <Step number="2" title="Install dependencies">
                        <code className="block bg-black/60 p-2 rounded mt-2">npm install</code>
                      </Step>
                      <Step number="3" title="Configure environment (optional)">
                        <p className="text-sm text-gray-400 mt-2">Create <code className="text-cyan-400">.env.local</code>:</p>
                        <code className="block bg-black/60 p-2 rounded mt-2">NEXT_PUBLIC_API_URL=http://127.0.0.1:8000</code>
                      </Step>
                      <Step number="4" title="Start development server">
                        <code className="block bg-black/60 p-2 rounded mt-2">npm run dev</code>
                      </Step>
                    </div>
                  </Section>

                  <Section title="Usage">
                    <div className="space-y-3">
                      <p>Once both servers are running:</p>
                      <ul className="list-disc list-inside space-y-2 ml-4">
                        <li>Backend API: <code className="text-cyan-400">http://localhost:8000</code></li>
                        <li>API Documentation: <code className="text-cyan-400">http://localhost:8000/docs</code></li>
                        <li>Frontend: <code className="text-cyan-400">http://localhost:3000</code></li>
                      </ul>
                      <p className="mt-4">Open your browser and navigate to <code className="text-cyan-400">http://localhost:3000</code> to start verifying content!</p>
                    </div>
                  </Section>
                </CardContent>
              </Card>
            </TabsContent>

            {/* API Tab */}
            <TabsContent value="api" className="space-y-6">
              <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-cyan-400">API Reference</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6 text-gray-300">
                  <Section title="Base URL">
                    <code className="block bg-black/60 p-2 rounded">http://localhost:8000</code>
                    <p className="text-sm text-gray-400 mt-2">For production, replace with your server URL.</p>
                  </Section>

                  <Section title="Interactive Documentation">
                    <p>When the backend is running, interactive API documentation is available at:</p>
                    <ul className="list-disc list-inside space-y-2 ml-4 mt-2">
                      <li>Swagger UI: <code className="text-cyan-400">http://localhost:8000/docs</code></li>
                      <li>ReDoc: <code className="text-cyan-400">http://localhost:8000/redoc</code></li>
                    </ul>
                  </Section>

                  <Section title="Endpoints">
                    <Endpoint 
                      method="POST" 
                      path="/verify/text" 
                      description="Verify factual claims in text content"
                      example={`curl -X POST "http://localhost:8000/verify/text" \\\n  -H "Content-Type: application/json" \\\n  -d '{"text": "The Earth orbits the Sun."}'`}
                    />
                    <Endpoint 
                      method="POST" 
                      path="/verify/url" 
                      description="Verify content from a URL"
                      example={`curl -X POST "http://localhost:8000/verify/url" \\\n  -H "Content-Type: application/json" \\\n  -d '{"url": "https://example.com/article"}'`}
                    />
                    <Endpoint 
                      method="POST" 
                      path="/verify/file" 
                      description="Verify content from uploaded file (PDF/DOCX)"
                      example={`curl -X POST "http://localhost:8000/verify/file" \\\n  -F "file=@document.pdf"`}
                    />
                    <Endpoint 
                      method="GET" 
                      path="/progress/{task_id}" 
                      description="Get progress status for a verification task"
                      example={`curl "http://localhost:8000/progress/your-task-id"`}
                    />
                  </Section>

                  <Section title="Response Format">
                    <code className="block bg-black/60 p-2 rounded text-xs overflow-x-auto">
{`{
  "task_id": "uuid-string",
  "domain": "general",
  "total_claims": 3,
  "overall_reliability": 0.85,
  "claims": [...],
  "extracted_citations": {...},
  "citation_verification": {...}
}`}
                    </code>
                  </Section>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Privacy Tab */}
            <TabsContent value="privacy" className="space-y-6">
              <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-cyan-400">Privacy Policy</CardTitle>
                  <p className="text-sm text-gray-400">Last Updated: January 2025</p>
                </CardHeader>
                <CardContent className="space-y-6 text-gray-300">
                  <Section title="Data Collection and Usage">
                    <p>When you use VibeVerifier, we process:</p>
                    <ul className="list-disc list-inside space-y-2 ml-4 mt-2">
                      <li><strong>Input Content:</strong> The text, URLs, or files you submit for verification</li>
                      <li><strong>Verification Results:</strong> The verification results, claims, and scores generated</li>
                      <li><strong>Usage Data:</strong> API usage patterns, timestamps, and technical logs</li>
                    </ul>
                  </Section>

                  <Section title="Data Storage">
                    <ul className="list-disc list-inside space-y-2 ml-4">
                      <li><strong>Temporary Storage:</strong> Input content is processed in memory and not permanently stored</li>
                      <li><strong>Cache:</strong> Search results and model data may be cached for performance</li>
                      <li><strong>Logs:</strong> Technical logs may be retained for debugging (typically 30 days)</li>
                    </ul>
                  </Section>

                  <Section title="Third-Party Services">
                    <div className="space-y-3">
                      <div>
                        <p><strong>Tavily API:</strong> Used for web search and source verification. Your content queries are sent to Tavily to retrieve verification sources.</p>
                        <a href="https://tavily.com/privacy" target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:underline text-sm flex items-center gap-1">
                          Review Tavily's Privacy Policy <ExternalLink className="h-3 w-3" />
                        </a>
                      </div>
                      <p><strong>Hugging Face Models:</strong> Pre-trained models are downloaded and run locally. Your content is not sent to Hugging Face servers.</p>
                    </div>
                  </Section>

                  <Section title="Self-Hosted Instances">
                    <p>If you are running a self-hosted instance:</p>
                    <ul className="list-disc list-inside space-y-2 ml-4 mt-2">
                      <li>You control all data on your infrastructure</li>
                      <li>No external data sharing</li>
                      <li>You manage your own API keys</li>
                      <li>You are responsible for your own privacy practices</li>
                    </ul>
                  </Section>

                  <Section title="Your Rights">
                    <p>Depending on your jurisdiction, you may have the right to:</p>
                    <ul className="list-disc list-inside space-y-2 ml-4 mt-2">
                      <li>Access your data</li>
                      <li>Request deletion of your data</li>
                      <li>Request correction of inaccurate data</li>
                      <li>Request a copy of your data in a portable format</li>
                    </ul>
                  </Section>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Credits Tab */}
            <TabsContent value="credits" className="space-y-6">
              <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-cyan-400">Credits & Acknowledgments</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6 text-gray-300">
                  <Section title="Development Team">
                    <p><strong>VibeCoders</strong></p>
                    <p className="text-sm text-gray-400">Development and maintenance of VibeVerifier</p>
                  </Section>

                  <Section title="Key Technologies">
                    <div className="space-y-3">
                      <div>
                        <p><strong>Backend:</strong></p>
                        <ul className="list-disc list-inside space-y-1 ml-4 text-sm">
                          <li>FastAPI - Web framework</li>
                          <li>Transformers & Sentence-Transformers - NLP models</li>
                          <li>PyTorch - Deep learning framework</li>
                          <li>Tavily API - Web search</li>
                        </ul>
                      </div>
                      <div>
                        <p><strong>Frontend:</strong></p>
                        <ul className="list-disc list-inside space-y-1 ml-4 text-sm">
                          <li>Next.js - React framework</li>
                          <li>Tailwind CSS - Styling</li>
                          <li>ShadCN UI - Component library</li>
                          <li>TypeScript - Type safety</li>
                        </ul>
                      </div>
                    </div>
                  </Section>

                  <Section title="Open Source Community">
                    <p>We extend our gratitude to:</p>
                    <ul className="list-disc list-inside space-y-2 ml-4 mt-2">
                      <li>The open-source community for creating excellent tools and libraries</li>
                      <li>Contributors to FastAPI, Next.js, React, and all dependencies</li>
                      <li>The Hugging Face community for providing state-of-the-art models</li>
                      <li>All developers who have contributed to the projects we rely on</li>
                    </ul>
                  </Section>

                  <Section title="License">
                    <p>This project is licensed under the <strong>MIT License</strong>.</p>
                    <p className="text-sm text-gray-400 mt-2">All third-party libraries retain their respective licenses. Please refer to individual library licenses for more information.</p>
                  </Section>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Team Tab */}
            <TabsContent value="team" className="space-y-6">
              <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-cyan-400">Project Makers</CardTitle>
                  <p className="text-sm text-gray-400">Meet the creators of VibeVerifier</p>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="flex justify-center items-center py-12">
                      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-400"></div>
                    </div>
                  ) : (
                    <div className="grid md:grid-cols-2 gap-8">
                      {contributors.map((contributor) => {
                        const contributorInfo = CONTRIBUTORS.find(c => c.username === contributor.login);
                        return (
                          <div key={contributor.login} className="flex flex-col items-center text-center p-6 bg-black/60 rounded-lg border border-cyan-500/30 h-full">
                            {/* Avatar */}
                            <div className="relative mb-4">
                              <img
                                src={contributor.avatar_url}
                                alt={contributorInfo?.name || contributor.name || contributor.login}
                                className="w-32 h-32 rounded-full border-4 border-cyan-500/50 object-cover shadow-lg"
                              />
                              <div className="absolute -bottom-2 -right-2 w-8 h-8 bg-gradient-to-r from-cyan-500 to-pink-500 rounded-full flex items-center justify-center">
                                <Github className="h-5 w-5 text-white" />
                              </div>
                            </div>
                            
                            {/* Name */}
                            <div className="mb-4">
                              <h3 className="text-2xl font-bold text-cyan-400">
                                {contributorInfo?.name || contributor.name || contributor.login}
                              </h3>
                              <p className="text-gray-400 text-sm">@{contributor.login}</p>
                            </div>
                            
                            {/* Bio - Always render with fixed height */}
                            <div className="mb-4 min-h-[3rem] flex items-center justify-center">
                              {contributor.bio ? (
                                <p className="text-gray-300 text-sm max-w-md">
                                  {contributor.bio}
                                </p>
                              ) : (
                                <p className="text-gray-500 text-sm italic">No bio available</p>
                              )}
                            </div>
                            
                            {/* Location - Always render with fixed height */}
                            <div className="mb-4 min-h-[1.5rem] flex items-center justify-center">
                              {contributor.location ? (
                                <p className="text-gray-400 text-xs flex items-center justify-center gap-1">
                                  📍 {contributor.location}
                                </p>
                              ) : (
                                <span className="text-transparent text-xs">📍</span>
                              )}
                            </div>
                            
                            {/* Stats */}
                            <div className="flex gap-6 mb-6">
                              <div className="text-center">
                                <p className="text-cyan-400 font-semibold">{contributor.public_repos}</p>
                                <p className="text-xs text-gray-400">Repositories</p>
                              </div>
                              <div className="text-center">
                                <p className="text-pink-400 font-semibold">{contributor.followers}</p>
                                <p className="text-xs text-gray-400">Followers</p>
                              </div>
                              <div className="text-center">
                                <p className="text-purple-400 font-semibold">{contributor.following}</p>
                                <p className="text-xs text-gray-400">Following</p>
                              </div>
                            </div>
                            
                            {/* GitHub Link - Always at bottom */}
                            <div className="mt-auto w-full">
                              <a
                                href={contributor.html_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center justify-center gap-2 w-full px-4 py-2 bg-gradient-to-r from-cyan-500/20 to-pink-500/20 border border-cyan-500/30 text-cyan-400 rounded-lg hover:from-cyan-500/30 hover:to-pink-500/30 transition-all"
                              >
                                <Github className="h-4 w-4" />
                                View GitHub Profile
                                <ExternalLink className="h-3 w-3" />
                              </a>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            {/* GitHub Tab */}
            <TabsContent value="github" className="space-y-6">
              <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-cyan-400">GitHub Repository</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6 text-gray-300">
                  <Section title="Open Source Project">
                    <p>VibeVerifier is an open-source project. The source code is available on GitHub.</p>
                    <div className="mt-4 p-4 bg-black/60 rounded-lg border border-cyan-500/30">
                      <div className="flex items-center gap-3">
                        <Github className="h-8 w-8 text-cyan-400" />
                        <div>
                          <p className="font-semibold text-cyan-400">VibeVerifier</p>
                          <p className="text-sm text-gray-400">Universal AI Hallucination & Citation Verification System</p>
                        </div>
                      </div>
                      <p className="mt-4 text-sm">
                        <strong>Repository:</strong> <a href={GITHUB_REPO_URL} target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:underline">{GITHUB_REPO_URL.replace('https://', '')}</a>
                      </p>
                      <p className="text-sm mt-2">
                        <strong>License:</strong> MIT License
                      </p>
                    </div>
                  </Section>

                  <Section title="Contributing">
                    <p>We welcome contributions! Here's how you can help:</p>
                    <ul className="list-disc list-inside space-y-2 ml-4 mt-2">
                      <li>⭐ Star the repository</li>
                      <li>🐛 Report bugs and issues</li>
                      <li>💡 Suggest new features</li>
                      <li>🤝 Submit pull requests</li>
                      <li>📝 Improve documentation</li>
                    </ul>
                    <p className="text-sm text-gray-400 mt-4">Please follow the contributing guidelines when submitting PRs.</p>
                  </Section>

                  <Section title="Links">
                    <div className="space-y-2">
                      <a href={GITHUB_REPO_URL} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300 transition-colors">
                        <Github className="h-4 w-4" />
                        View on GitHub
                        <ExternalLink className="h-3 w-3" />
                      </a>
                      <a href={`${GITHUB_REPO_URL}/issues`} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300 transition-colors">
                        <Github className="h-4 w-4" />
                        Report an Issue
                        <ExternalLink className="h-3 w-3" />
                      </a>
                      <a href={`${GITHUB_REPO_URL}/pulls`} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300 transition-colors">
                        <Github className="h-4 w-4" />
                        Submit a Pull Request
                        <ExternalLink className="h-3 w-3" />
                      </a>
                    </div>
                  </Section>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Back to Home */}
          <div className="text-center pt-8">
            <Link 
              href="/"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-pink-500 text-white rounded-lg hover:from-cyan-600 hover:to-pink-600 transition-all font-semibold"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}

// Helper Components
function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <h3 className="text-xl font-semibold text-cyan-400">{title}</h3>
      <div>{children}</div>
    </div>
  );
}

function Step({ number, title, children }: { number: string; title: string; children: React.ReactNode }) {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-pink-500 flex items-center justify-center font-bold text-white">
        {number}
      </div>
      <div className="flex-1">
        <h4 className="font-semibold text-white">{title}</h4>
        {children}
      </div>
    </div>
  );
}

function Endpoint({ method, path, description, example }: { method: string; path: string; description: string; example: string }) {
  return (
    <div className="p-4 bg-black/60 rounded-lg border border-cyan-500/30">
      <div className="flex items-center gap-3 mb-2">
        <span className={`px-2 py-1 rounded text-xs font-semibold ${
          method === 'GET' ? 'bg-green-500/20 text-green-400' :
          method === 'POST' ? 'bg-blue-500/20 text-blue-400' :
          'bg-gray-500/20 text-gray-400'
        }`}>
          {method}
        </span>
        <code className="text-cyan-400">{path}</code>
      </div>
      <p className="text-sm text-gray-400 mb-3">{description}</p>
      <code className="block bg-black/80 p-3 rounded text-xs overflow-x-auto">{example}</code>
    </div>
  );
}

