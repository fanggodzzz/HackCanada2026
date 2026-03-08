import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { UploadCloud, Image as ImageIcon, X } from "lucide-react";
import api from "../api";

export default function Scan() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [bodyPosition, setBodyPosition] = useState("Face");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFile = (selectedFile) => {
    if (selectedFile && selectedFile.type.startsWith("image/")) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setError("");
    } else {
      setError("Please upload a valid image file (JPEG, PNG).");
    }
  };

  const onDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleClear = () => {
    setFile(null);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleScan = async () => {
    if (!file) return setError("Please upload an image.");

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("body_position", bodyPosition);

    try {
      const response = await api.post("/scan", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      navigate("/results", { state: { result: response.data } });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Analysis failed. Model may not be trained yet.",
      );
    } finally {
      setLoading(false);
    }
  };

  const bodyParts = ["Arm"];

  return (
    <div className="container flex justify-center py-12">
      <div className="glass-card max-w-2xl w-full animate-fade-in mt-8">
        <h2 className="text-3xl font-bold mb-6 text-center">New AI Scan</h2>

        {error && (
          <div className="p-4 mb-4 rounded bg-red-900/30 text-danger border border-red-500/50">
            {error}
          </div>
        )}

        {!preview ? (
          <div
            className={`upload-zone ${dragActive ? "active" : ""}`}
            onDragEnter={onDrag}
            onDragLeave={onDrag}
            onDragOver={onDrag}
            onDrop={onDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={(e) => handleFile(e.target.files[0])}
              className="hidden"
              style={{ display: "none" }}
            />
            <div className="flex flex-col items-center">
              <UploadCloud className="upload-icon" />
              <p className="text-xl font-bold mb-2">Drag & Drop Image Here</p>
              <p className="text-muted mb-4">
                or click to browse from your device
              </p>
              <button className="btn-outline text-sm">Select File</button>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center mb-6">
            <div className="relative w-full max-w-md mx-auto aspect-video">
              <img
                src={preview}
                alt="Upload preview"
                className="preview-image w-full h-auto max-h-[400px] object-contain rounded-lg border border-slate-700"
              />
              <button
                onClick={handleClear}
                className="absolute top-2 right-2 p-2 bg-red-500/90 hover:bg-red-600 text-white rounded-full transition shadow-lg"
                title="Remove image"
              >
                <X size={20} />
              </button>
            </div>
          </div>
        )}

        <div className="form-group mt-6">
          <label>Where is this condition located?</label>
          <select
            value={bodyPosition}
            onChange={(e) => setBodyPosition(e.target.value)}
            className="w-full bg-slate-800/50 border border-slate-700 text-white p-3 rounded-lg outline-none focus:border-primary transition"
          >
            {bodyParts.map((part) => (
              <option key={part} value={part} className="bg-slate-800">
                {part}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleScan}
          className="btn-primary w-full mt-4 flex justify-center items-center gap-2 text-lg py-3 shadow-lg hover:shadow-primary/20"
          disabled={!file || loading}
        >
          {loading ? (
            <>Processing... (This may take a moment)</>
          ) : (
            <>
              <ImageIcon size={20} /> Analyze Condition
            </>
          )}
        </button>
      </div>
    </div>
  );
}
