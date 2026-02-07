"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import api from "../../lib/api";
import { Send, CheckCircle, Circle, Trash2, LogOut, Bot, User } from "lucide-react";

interface Task {
  id: number;
  title: string;
  completed: boolean;
}

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Dashboard() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  
  // Auto-scroll for chat
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 1. Initial Load (Check Login & Fetch Tasks)
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const storedUserId = localStorage.getItem("user_id");
    
    if (!token || !storedUserId) {
      router.push("/");
      return;
    }
    setUserId(storedUserId);
    fetchTasks(storedUserId);
    
    // Welcome Message
    setMessages([{ role: "assistant", content: "Hello! I am your AI Task Manager. Tell me what to do!" }]);
  }, []);

  // Scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // --- API FUNCTIONS ---

  const fetchTasks = async (uid: string) => {
    try {
      const res = await api.get(`/${uid}/tasks`);
      setTasks(res.data);
    } catch (err) {
      console.error("Failed to fetch tasks", err);
    }
  };

  const toggleTask = async (taskId: number) => {
    try {
      // Optimistic Update (UI updates immediately)
      setTasks(tasks.map(t => t.id === taskId ? { ...t, completed: !t.completed } : t));
      await api.patch(`/${userId}/tasks/${taskId}/complete`);
    } catch (err) {
      fetchTasks(userId!); // Revert on error
    }
  };

  const deleteTask = async (taskId: number) => {
    if (!confirm("Are you sure?")) return;
    try {
      setTasks(tasks.filter(t => t.id !== taskId));
      await api.delete(`/${userId}/tasks/${taskId}`);
    } catch (err) {
      fetchTasks(userId!);
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input;
    setInput("");
    
    // Add User Message to UI
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      // Call AI
      const res = await api.post("/chat", { message: userMsg });
      
      // Add AI Response to UI
      setMessages(prev => [...prev, { role: "assistant", content: res.data.response }]);
      
      // IMPORTANT: Refresh tasks because AI might have added/deleted something
      if (userId) fetchTasks(userId);

    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", content: "Sorry, something went wrong." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    router.push("/");
  };

  return (
    <div className="flex h-screen bg-gray-950 text-white overflow-hidden">
      
      {/* LEFT PANEL: TASK LIST */}
      <div className="w-1/3 border-r border-gray-800 flex flex-col bg-gray-900">
        <div className="p-6 border-b border-gray-800 flex justify-between items-center">
          <h2 className="text-xl font-bold text-blue-400">My Tasks</h2>
          <button onClick={handleLogout} className="text-gray-500 hover:text-red-400">
            <LogOut size={20} />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {tasks.length === 0 ? (
            <div className="text-center text-gray-600 mt-10">No tasks yet. Ask AI to add one!</div>
          ) : (
            tasks.map(task => (
              <div key={task.id} className="flex items-center justify-between bg-gray-800 p-3 rounded-lg border border-gray-700 group hover:border-blue-500/50 transition">
                <div className="flex items-center gap-3 overflow-hidden">
                  <button onClick={() => toggleTask(task.id)} className="text-gray-400 hover:text-green-400 flex-shrink-0">
                    {task.completed ? <CheckCircle className="text-green-500" /> : <Circle />}
                  </button>
                  <span className={`truncate ${task.completed ? "line-through text-gray-500" : "text-gray-200"}`}>
                    {task.title}
                  </span>
                </div>
                <button onClick={() => deleteTask(task.id)} className="text-gray-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition">
                  <Trash2 size={18} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      {/* RIGHT PANEL: AI CHAT */}
      <div className="flex-1 flex flex-col bg-gray-950">
        {/* Chat Header */}
        <div className="p-4 border-b border-gray-800 bg-gray-900/50">
          <h2 className="font-semibold flex items-center gap-2">
            <Bot className="text-purple-500" /> AI Assistant (Gemini 2.5 Flash)
          </h2>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[80%] p-4 rounded-2xl ${
                m.role === "user" 
                  ? "bg-blue-600 text-white rounded-br-none" 
                  : "bg-gray-800 text-gray-200 rounded-bl-none border border-gray-700"
              }`}>
                <div className="flex items-center gap-2 mb-1 opacity-50 text-xs uppercase font-bold tracking-wider">
                  {m.role === "user" ? <User size={12}/> : <Bot size={12}/>} 
                  {m.role}
                </div>
                <div className="whitespace-pre-wrap leading-relaxed">{m.content}</div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 p-4 rounded-2xl rounded-bl-none animate-pulse text-gray-400 text-sm">
                Thinking...
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 bg-gray-900 border-t border-gray-800">
          <form onSubmit={sendMessage} className="flex gap-2 relative">
            <input
              className="flex-1 bg-gray-800 text-white rounded-xl px-4 py-3 border border-gray-700 focus:ring-2 focus:ring-purple-500 outline-none pr-12"
              placeholder="Ex: Add a meeting with Ayesha tomorrow at 10 AM..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button 
              type="submit" 
              disabled={loading || !input.trim()}
              className="absolute right-2 top-2 p-1.5 bg-purple-600 hover:bg-purple-700 rounded-lg text-white disabled:opacity-50 transition"
            >
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}