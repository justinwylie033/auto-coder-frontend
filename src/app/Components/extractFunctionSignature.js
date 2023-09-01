function extractFunctionSignature(description) {
  // Default to "Description" if no suitable function signature is found.
  if (!description || typeof description !== "string") {
    return "Description";
  }

  // Create a regular expression pattern to match function signatures like:
  // `functionName(parameters)`
  const regexPattern = /`([a-zA-Z_]\w*)\(([^`]*?)\)`/;

  const matches = description.match(regexPattern);

  // If we have matches, structure and return the function signature
  if (matches) {
    const functionName = matches[1].trim();
    const parameters = matches[2].split(',').map(param => param.trim()).filter(Boolean).join(', ');
    return `${functionName}(${parameters})`;
  }

  return "Description";  // Default response if no matches are found.
}

export default extractFunctionSignature;
