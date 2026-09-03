import React, { useState, useEffect } from "react";
import { Button } from "../ui/button";
import { z } from "zod";
import { motion, AnimatePresence } from "framer-motion";

interface ProfileFormProps {
  onSubmit: (designation: string, profileText: string, department?: string, education?: string, trainingHistory?: string[]) => void;
  isLoading: boolean;
}

const profileSchema = z.object({
  designation: z.string().min(2, "Designation must be at least 2 characters"),
  department: z.string().optional(),
  education: z.string().optional(),
  trainingHistory: z.string().optional(), // We'll split this by comma
  profileText: z.string().min(5, "Profile text must be at least 5 characters"),
});

type FormErrors = {
  designation?: string;
  profileText?: string;
};

const ProfileForm: React.FC<ProfileFormProps> = ({ onSubmit, isLoading }) => {
  const [designation, setDesignation] = useState("");
  const [department, setDepartment] = useState("");
  const [education, setEducation] = useState("");
  const [trainingHistory, setTrainingHistory] = useState("");
  const [profileText, setProfileText] = useState("");
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState({ designation: false, profileText: false });

  useEffect(() => {
    const result = profileSchema.safeParse({ designation, profileText });
    if (!result.success) {
      const fieldErrors: FormErrors = {};
      result.error.issues.forEach((issue) => {
        if (issue.path[0] === "designation") fieldErrors.designation = issue.message;
        if (issue.path[0] === "profileText") fieldErrors.profileText = issue.message;
      });
      setErrors(fieldErrors);
    } else {
      setErrors({});
    }
  }, [designation, profileText]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const result = profileSchema.safeParse({ designation, profileText, department, education, trainingHistory });
    if (result.success) {
      const historyList = trainingHistory ? trainingHistory.split(',').map(s => s.trim()).filter(Boolean) : undefined;
      onSubmit(designation, profileText, department, education, historyList);
    }
  };

  const isValid = !errors.designation && !errors.profileText && designation.length > 0 && profileText.length > 0;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <div className="flex justify-between items-end ml-1">
          <label className="text-[10px] font-black text-zinc-100 uppercase tracking-widest">
            Designation / Role
          </label>
          <AnimatePresence>
            {touched.designation && errors.designation && (
              <motion.span
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                className="text-[10px] font-bold text-red-400 uppercase tracking-tighter"
              >
                {errors.designation}
              </motion.span>
            )}
          </AnimatePresence>
        </div>
        <input
          type="text"
          value={designation}
          onChange={(e) => setDesignation(e.target.value)}
          onBlur={() => setTouched(prev => ({ ...prev, designation: true }))}
          placeholder="e.g. Statistical Officer"
          disabled={isLoading}
          className={`w-full font-sans bg-black/20 border rounded-2xl px-5 py-4 text-sm text-white placeholder:text-zinc-500 focus:outline-none transition-all disabled:opacity-50 ${
            touched.designation && errors.designation 
              ? "border-red-500/50 focus:border-red-500 focus:ring-1 focus:ring-red-500/20" 
              : "border-white/10 focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20"
          }`}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="text-[10px] font-black text-zinc-100 uppercase tracking-widest ml-1">Department / Cadre</label>
          <input
            type="text"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            placeholder="e.g. ISS, SSS"
            disabled={isLoading}
            className="w-full font-sans bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all disabled:opacity-50"
          />
        </div>

        <div className="space-y-2">
          <label className="text-[10px] font-black text-zinc-100 uppercase tracking-widest ml-1">Education</label>
          <input
            type="text"
            value={education}
            onChange={(e) => setEducation(e.target.value)}
            placeholder="e.g. MSc Statistics"
            disabled={isLoading}
            className="w-full font-sans bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all disabled:opacity-50"
          />
        </div>
      </div>

      <div className="space-y-2">
        <label className="text-[10px] font-black text-zinc-100 uppercase tracking-widest ml-1">Previous Trainings (comma-separated)</label>
        <input
          type="text"
          value={trainingHistory}
          onChange={(e) => setTrainingHistory(e.target.value)}
          placeholder="e.g. iGOT Data Privacy, Basic SQL"
          disabled={isLoading}
          className="w-full font-sans bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all disabled:opacity-50"
        />
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-end ml-1">
          <label className="text-[10px] font-black text-zinc-100 uppercase tracking-widest">
            Professional Background & Duties
          </label>
          <AnimatePresence>
            {touched.profileText && errors.profileText && (
              <motion.span
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                className="text-[10px] font-bold text-red-400 uppercase tracking-tighter"
              >
                {errors.profileText}
              </motion.span>
            )}
          </AnimatePresence>
        </div>
        <textarea
          value={profileText}
          onChange={(e) => setProfileText(e.target.value)}
          onBlur={() => setTouched(prev => ({ ...prev, profileText: true }))}
          placeholder="Describe your current duties, field operations, or technical tasks..."
          disabled={isLoading}
          rows={6}
          className={`w-full font-sans bg-black/20 border rounded-2xl px-5 py-4 text-sm text-white placeholder:text-zinc-500 focus:outline-none transition-all resize-none disabled:opacity-50 ${
            touched.profileText && errors.profileText 
              ? "border-red-500/50 focus:border-red-500 focus:ring-1 focus:ring-red-500/20" 
              : "border-white/10 focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20"
          }`}
        />
      </div>

      <Button 
        type="submit" 
        disabled={isLoading || !isValid}
        className={`w-full font-sans h-16 rounded-2xl font-black uppercase tracking-[0.2em] text-[11px] transition-all duration-500 border ${
          isLoading || !isValid
            ? "bg-zinc-800 text-zinc-500 border-white/5 cursor-not-allowed opacity-50" 
            : "bg-white text-black border-cyan-400 hover:bg-cyan-400 hover:text-white hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_20px_rgba(34,211,238,0.4)]"
        }`}
      >
        {isLoading ? (
          <span className="flex items-center gap-3">
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            System Processing...
          </span>
        ) : (
          "Generate Learning Plan"
        )}
      </Button>
    </form>
  );
};

export default ProfileForm;
