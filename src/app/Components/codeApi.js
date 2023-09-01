import { apiRequest } from "./api";

export const generateCode = async (prompt) => {
    return await apiRequest("generate-code", { prompt });
};

export const installPackages = async (code) => {
    return await apiRequest("install-packages", { code });
};

export const executeCode = async (code) => {
    return await apiRequest("execute-code", { code });
};

export const fixCode = async (code, errorInfo) => {
    return await apiRequest("fix-code", { code, info: errorInfo });
};

export const describeFunction = async (code) => {
    return await apiRequest("describe-function", { code });
};
