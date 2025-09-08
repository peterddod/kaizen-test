import axios from 'axios';

export const analyseContent = async (content, clientName, campaignName, campaignUrl) => {
  const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/analyse`, {
    content,
    client_name: clientName,
    campaign_name: campaignName,
    campaign_url: campaignUrl
  });
  return response.data;
};

export const analyseFile = async (file, clientName, campaignName, campaignUrl) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('client_name', clientName);
  if (campaignName) {
    formData.append('campaign_name', campaignName);
  }
  if (campaignUrl) {
    formData.append('campaign_url', campaignUrl);
  }

  const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/analyse-file`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};