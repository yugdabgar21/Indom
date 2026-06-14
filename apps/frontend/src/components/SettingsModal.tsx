"use client";

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { API_BASE_URL } from '@/lib/config';

interface ModelInfo {
  id: string;
  name: string;
  free: boolean;
}

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

  // Model fetching state
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [modelCount, setModelCount] = useState(0);
  const [fetchingModels, setFetchingModels] = useState(false);
  const [fetchError, setFetchError] = useState('');
  const [modelSearch, setModelSearch] = useState('');
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<NodeJS.Timeout | null>(null);

  // Load settings on open
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

  // Auto-fetch models when provider or API key changes
  const fetchModels = useCallback(async (provider: string, key: string) => {
    if (!key || key.length < 5) {
      setModels([]);
      setModelCount(0);
      setFetchError('');
      return;
    }

    setFetchingModels(true);
    setFetchError('');

    try {
      const resp = await fetch(`${API_BASE_URL}/api/models`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider, api_key: key }),
      });
      const data = await resp.json();

      if (data.error) {
        setFetchError(data.error);
        setModels([]);
        setModelCount(0);
      } else {
        setModels(data.models || []);
        setModelCount(data.count || 0);
        setFetchError('');
      }
    } catch {
      setFetchError('Failed to connect');
      setModels([]);
      setModelCount(0);
    } finally {
      setFetchingModels(false);
    }
  }, []);

  // Debounced fetch trigger
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      fetchModels(modelProvider, apiKey);
    }, 800);
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [modelProvider, apiKey, fetchModels]);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filter models by search query
  const filteredModels = models.filter(m => {
    const q = modelSearch.toLowerCase();
    return m.id.toLowerCase().includes(q) || m.name.toLowerCase().includes(q) ||
      (q === 'free' && m.free);
  });

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
    } catch {
      alert("Failed to save settings.");
    } finally {
      setSaving(false);
    }
  };

  const providerConfig: Record<string, { label: string; placeholder: string; link: string; linkText: string }> = {
    'openrouter': { label: 'OpenRouter API Key', placeholder: 'sk-or-v1-...', link: 'https://openrouter.ai/keys', linkText: 'openrouter.ai/keys' },
    'opencode-zen': { label: 'OpenCode Zen API Key', placeholder: 'zen-...', link: 'https://opencode.ai/auth', linkText: 'opencode.ai/auth' },
    'openai': { label: 'OpenAI API Key', placeholder: 'sk-...', link: 'https://platform.openai.com/api-keys', linkText: 'platform.openai.com' },
    'anthropic': { label: 'Anthropic API Key', placeholder: 'sk-ant-...', link: 'https://console.anthropic.com/keys', linkText: 'console.anthropic.com' },
    'gemini': { label: 'Google Gemini API Key', placeholder: 'AIza...', link: 'https://aistudio.google.com/apikey', linkText: 'aistudio.google.com' },
  };

  const currentProvider = providerConfig[modelProvider] || providerConfig['openrouter'];

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
            {/* Model Provider */}
            <div>
              <label className="text-xs font-heading uppercase text-[#888] mb-1 block">
                Model Provider
              </label>
              <select
                value={modelProvider}
                onChange={(e) => {
                  setModelProvider(e.target.value);
                  setModels([]);
                  setModelCount(0);
                  setModelSearch('');
                  setDropdownOpen(false);
                }}
                className="w-full bg-[#111] brutal-border p-3 text-sm font-mono text-foreground focus:outline-none focus:border-accent"
              >
                <option value="openrouter">OpenRouter</option>
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="gemini">Google Gemini</option>
                <option value="opencode-zen">OpenCode Zen</option>
              </select>
            </div>

            {/* API Key */}
            <div>
              <label className="text-xs font-heading uppercase text-[#888] mb-1 block">
                {currentProvider.label}
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder={currentProvider.placeholder}
                className="w-full bg-[#111] brutal-border p-3 text-sm font-mono text-foreground focus:outline-none focus:border-accent"
              />
              <div className="flex items-center justify-between mt-1">
                <p className="text-xs text-[#555]">
                  Get yours at{' '}
                  <a href={currentProvider.link} target="_blank" rel="noreferrer" className="text-accent hover:underline">
                    {currentProvider.linkText}
                  </a>
                </p>
                {/* Model count / status badge */}
                {fetchingModels && (
                  <span className="text-xs text-accent animate-pulse font-mono">Fetching...</span>
                )}
                {!fetchingModels && fetchError && (
                  <span className="text-xs text-red-400 font-mono">⚠ {fetchError}</span>
                )}
                {!fetchingModels && !fetchError && modelCount > 0 && (
                  <span className="text-xs text-green-400 font-mono">✓ {modelCount} models</span>
                )}
              </div>
            </div>

            {/* Model Selection — searchable dropdown or text input */}
            <div ref={dropdownRef} className="relative">
              <label className="text-xs font-heading uppercase text-[#888] mb-1 block">
                Select Model
              </label>

              {models.length > 0 ? (
                <>
                  {/* Selected model display / trigger */}
                  <button
                    type="button"
                    onClick={() => setDropdownOpen(!dropdownOpen)}
                    className="w-full bg-[#111] brutal-border p-3 text-sm font-mono text-foreground text-left flex items-center justify-between focus:outline-none focus:border-accent hover:border-accent/50 transition-colors"
                  >
                    <span className={modelName ? 'text-foreground' : 'text-[#555]'}>
                      {modelName || 'Click to select a model...'}
                    </span>
                    <svg className={`w-4 h-4 text-[#555] transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {/* Dropdown */}
                  {dropdownOpen && (
                    <div className="absolute z-50 w-full mt-1 bg-[#0a0a0a] brutal-border brutal-shadow max-h-64 flex flex-col">
                      {/* Search input */}
                      <div className="p-2 border-b border-[#333]">
                        <input
                          type="text"
                          value={modelSearch}
                          onChange={(e) => setModelSearch(e.target.value)}
                          placeholder="🔍 Search models... (try 'free')"
                          className="w-full bg-[#111] border border-[#333] p-2 text-xs font-mono text-foreground focus:outline-none focus:border-accent rounded-none"
                          autoFocus
                        />
                      </div>
                      {/* Model list */}
                      <div className="overflow-y-auto max-h-48 scrollbar-thin">
                        {filteredModels.length === 0 ? (
                          <div className="p-3 text-xs text-[#555] text-center font-mono">No models match &quot;{modelSearch}&quot;</div>
                        ) : (
                          filteredModels.map((m) => (
                            <button
                              key={m.id}
                              type="button"
                              onClick={() => {
                                setModelName(m.id);
                                setDropdownOpen(false);
                                setModelSearch('');
                              }}
                              className={`w-full text-left px-3 py-2 text-xs font-mono flex items-center justify-between hover:bg-accent/10 transition-colors ${
                                modelName === m.id ? 'bg-accent/20 text-accent' : 'text-foreground'
                              }`}
                            >
                              <span className="truncate mr-2">{m.id}</span>
                              {m.free && (
                                <span className="shrink-0 text-[10px] px-1.5 py-0.5 bg-green-500/20 text-green-400 border border-green-500/30 font-bold uppercase">
                                  Free
                                </span>
                              )}
                            </button>
                          ))
                        )}
                      </div>
                    </div>
                  )}
                </>
              ) : (
                /* Fallback: plain text input when no models fetched */
                <>
                  <input
                    type="text"
                    value={modelName}
                    onChange={(e) => setModelName(e.target.value)}
                    placeholder={modelProvider === 'opencode-zen' ? 'big-pickle' : 'google/gemma-4-31b-it:free'}
                    className="w-full bg-[#111] brutal-border p-3 text-sm font-mono text-foreground focus:outline-none focus:border-accent"
                  />
                  <p className="text-xs text-[#555] mt-1">
                    {apiKey
                      ? 'Enter API key above to browse available models'
                      : modelProvider === 'opencode-zen'
                        ? 'Free: big-pickle, deepseek-v4-flash-free, mimo-v2.5-free'
                        : 'Free: gemma-4-31b-it:free, nemotron-nano-9b-v2:free, gpt-oss-20b:free'}
                  </p>
                </>
              )}
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
