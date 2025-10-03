import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

export function MCQChallenge({ challenge, showExplanation = false }) {
  const [selectedOption, setSelectedOption] = useState(null);
  const [shouldShowExplanation, setShouldShowExplanation] =
    useState(showExplanation);

  // 🔑 Reset state when a new challenge comes in
  useEffect(() => {
    setSelectedOption(null);
    setShouldShowExplanation(showExplanation);
  }, [challenge, showExplanation]);

  const options =
    typeof challenge.options === "string"
      ? JSON.parse(challenge.options)
      : challenge.options;

  const handleOptionSelect = (index) => {
    if (selectedOption !== null) return; // Prevent multiple answers
    setSelectedOption(index);
    setShouldShowExplanation(true);
  };

  const getOptionClass = (index) => {
    if (selectedOption === null) return "option";
    if (index === challenge.correct_answer_id) return "option correct";
    if (selectedOption === index && index !== challenge.correct_answer_id)
      return "option incorrect";
    return "option";
  };

  // ✅ helper: detect fenced code block
  const renderContent = (content) => {
    if (typeof content === "string" && content.includes("```")) {
      const code = content.replace(/```[a-z]*|```/g, "").trim();
      const langMatch = content.match(/```(\w+)/);
      const language = langMatch ? langMatch[1] : "text";

      return (
        <SyntaxHighlighter
          language={language}
          style={vscDarkPlus}
          className="code-block"
          customStyle={{ padding: "1rem", margin: "1rem 0" }}
        >
          {code}
        </SyntaxHighlighter>
      );
    }
    return <p>{content}</p>;
  };

  return (
    <div className="challenge-container">
      <p>
        <strong>Difficulty:</strong> {challenge.difficulty}
      </p>

      <h3 className="challenge-title">{challenge.title}</h3>

      <div className="challenge-body">{renderContent(challenge.body)}</div>

      <div className="options">
        {options.map((option, index) => (
          <div
            key={index}
            className={getOptionClass(index)}
            onClick={() => handleOptionSelect(index)}
          >
            {renderContent(option)}
          </div>
        ))}
      </div>

      <AnimatePresence>
        {shouldShowExplanation && selectedOption !== null && (
          <motion.div
            className="explanation"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            <h4>Explanation</h4>
            {renderContent(challenge.explanation)}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
