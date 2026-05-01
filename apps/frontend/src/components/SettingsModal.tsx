"use client";

import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '@/lib/config';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function SettingsModal({ isOpen, onClose }: SettingsModalProps) {
  const [apiKey, setApiKey] = useState('');
  const [modelProvider, setModelProvider] = useState('openrouter');
  const [modelName, setModelName] = useState('google/gemma-4-31b-it:free');
  const [searxngUrl, setSearxngUrl] = useState('http://localhost:8888');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      fetch(`${API_BASE_URL}/api/settings`)
        .then(res => res.json())
        .then(data => {
          setApiKey(data.api_key || '');
          setModelProvider(data.model_provider || 'openrouter');
          setModelName(data.model_name || 'google/gemma-4-31b-it:free');
          setSearxngUrl(data.searxng_url || 'http://localhost:8888');
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }
  }, [isOpen]);

  const handleSave = async () => {
    setSaving(true);
    try {
      await fetch(`${API_BASE_URL}/api/settings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          api_key: apiKey,
          model_provider: modelProvider,
          model_name: modelName,
          searxng_url: searxngUrl,
        }),
      });
      setSaved(true);
      setTimeout(() => { setSaved(false); onClose(); }, 1000);
    } catch (err) {
      alert("Failed to save settings.");
    } finally {
      setSaving(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <div className="brutal-border bg-background p-6 w-full max-w-lg brutal-shadow">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl text-accent font-heading uppercase">Settings</h2>
          <button onClick={onClose} className="text-[#888] hover:text-white text-xl font-bold">✕</button>
        </div>

        {loading ? (
          <div className="text-accent animate-pulse font-heading py-8 text-center">Loading...</div>
        ) : (
          <div className="flex flex-col gap-5">
            {/* API Key */}
            <div>
              <label className="text-xs font-heading uppercase text-[#888] mb-1 block">
                OpenRouter API Key
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-or-v1-..."
                className="w-full bg-[#111] brutal-border p-3 text-sm font-mono text-foreground focus:outline-none focus:border-accent"
              />
              <p className="text-xs text-[#555] mt-1">
                Get yours at{' '}
                <a href="https://openrouter.ai/keys" target="_blank" rel="noreferrer" className="text-accent hover:underline">
                  openrouter.ai/keys
                </a>
              </p>
            </div>

            {/* Model Provider */}
            <div>
              <label className="text-xs font-heading uppercase text-[#888] mb-1 block">
                Model Provider
              </label>
              <select
                value={modelProvider}
                onChange={(e) => setModelProvider(e.target.value)}
                className="w-full bg-[#111] brutal-border p-3 text-sm font-mono text-foreground focus:outline-none focus:border-accent"
              >
                <option value="openrouter">OpenRouter</option>
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="gemini">Google Gemini</option>
              </select>
            </div>

            {/* Model Name */}
            <div>
              <label className="text-xs font-heading uppercase text-[#888] mb-1 block">
                Model Name
              </label>
              <input
                type="text"
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                placeholder="google/gemma-4-31b-it:free"
                className="w-full bg-[#111] brutal-border p-3 text-sm font-mono text-foreground focus:outline-none focus:border-accent"
              />
              <p className="text-xs text-[#555] mt-1">Free models: gemma-4-31b-it:free, nemotron-nano-9b-v2:free, gpt-oss-20b:free</p>
            </div>

            {/* SearXNG URL */}
            <div>
              <label className="text-xs font-heading uppercase text-[#888] mb-1 block">
                SearXNG Instance URL
              </label>
              <input
                type="text"
                value={searxngUrl}
                onChange={(e) => setSearxngUrl(e.target.value)}
                placeholder="http://localhost:8888"
                className="w-full bg-[#111] brutal-border p-3 text-sm font-mono text-foreground focus:outline-none focus:border-accent"
              />
            </div>

            {/* Save Button */}
            <button
              onClick={handleSave}
              disabled={saving}
              className="w-full bg-accent text-background font-heading uppercase font-bold py-3 brutal-border border-accent hover:bg-accent/90 transition-colors disabled:opacity-50"
            >
              {saved ? '✓ Saved!' : saving ? 'Saving...' : 'Save Settings'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
