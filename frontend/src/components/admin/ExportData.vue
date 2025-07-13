<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title mb-4">Export Data</h4>

      <div class="mb-4">
        <p>Generate and download service request reports in CSV format.</p>
      </div>

      <div class="card mb-4">
        <div class="card-body">
          <h5 class="card-title">Service Requests Report</h5>
          <p class="card-text">Export all closed service requests data.</p>

          <div class="mb-3">
            <label for="dateRange" class="form-label">Date Range</label>
            <select class="form-select" id="dateRange" v-model="dateRange">
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 3 months</option>
              <option value="180">Last 6 months</option>
              <option value="365">Last year</option>
              <option value="all">All time</option>
            </select>
          </div>

          <button class="btn btn-primary" @click="exportServiceRequests" :disabled="exporting">
            <span v-if="exporting" class="spinner-border spinner-border-sm me-2"></span>
            Export as CSV
          </button>
        </div>
      </div>

      <!-- Chart Section -->
      <div class="card mb-4">
        <div class="card-body">
          <h5 class="card-title">Completed Requests Statistics</h5>
          <canvas ref="chartCanvas"></canvas>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import {nextTick } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  name: "ExportData",
  data() {
    return {
      dateRange: "30",
      exporting: false,
      exportJobs: [],
      chartCanvas: null,
      chartInstance: null,
      pollingInterval: null,
    };
  },
  mounted() {
    this.fetchExportJobs();
    this.fetchChartData();
    this.pollingInterval = setInterval(this.fetchExportJobs, 5000);
  },
  beforeUnmount() {
    clearInterval(this.pollingInterval);
    if (this.chartInstance) {
      this.chartInstance.destroy();
    }
  },
  methods: {
    async fetchExportJobs() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/admin/completed-service-requests/");
        this.exportJobs = response.data;
      } catch (error) {
        console.error("Error fetching export jobs:", error);
      }
    },

    async exportServiceRequests() {
      try {
        this.exporting = true;
        const response = await axios.get("http://127.0.0.1:5000/api/admin/completed-service-requests/");

        console.log("Response:", response.data);
        console.log("Exporting service details to CSV...");

        const services = response.data || [];
        console.log("Service Details:", services);
        const headers = [
      "Service ID",
      "Customer ID",
      "Professional ID",
      "Date of Request",
      "Date of Completion",
      "Scheduled Date",
      "Service Name",
      "Price",
      "Time Required",
      "Remarks",
      "Status",
    ];
        const rows = services.map((service) => [
  service.service_id,
  service.customer_id,
  service.professional_id,
  service.date_of_request,
  service.date_of_completion,
  service.scheduled_date,
  service.service?.name || "N/A",
  service.service?.price || "N/A",
  service.service?.time_required || "N/A",
  service.remarks || "N/A",
  service.status,
]);

        const csvContent =
          "data:text/csv;charset=utf-8," + [headers, ...rows].map(row => row.join(",")).join("\n");

        console.log("CSV Content:", csvContent);

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "service_details.csv");
        document.body.appendChild(link);

        link.click();
        document.body.removeChild(link);
        alert("Successful")
      } catch (error) {
        console.error("Error exporting service requests:", error);
        alert("Failed")
      } finally {
        this.exporting = false;
      }
    },

    async fetchChartData() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/admin/completed-service-requests");
        const data = response.data || [];

        const totalRequests = data.length;
        const completedRequests = data.filter(req => req.status === "completed").length;
        const pendingRequests = totalRequests - completedRequests;

        const chartData = {
          "Total Requests": totalRequests,
          "Completed Requests": completedRequests,
          "Pending Requests": pendingRequests,
        };

        console.log("Chart Data:", chartData);
        await nextTick();
        this.renderChart(chartData);
      } catch (error) {
        console.error("Error fetching chart data:", error);
      }
    },

    renderChart(data) {
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      this.chartInstance = new Chart(this.$refs.chartCanvas, {
        type: "bar",
        data: {
          labels: Object.keys(data),
          datasets: [
            {
              label: "Service Request Stats",
              data: Object.values(data),
              backgroundColor: ["rgba(75, 192, 192, 0.6)", "rgba(54, 162, 235, 0.6)", "rgba(255, 206, 86, 0.6)"],
              borderColor: ["rgba(75, 192, 192, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)"],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: { y: { beginAtZero: true } },
        },
      });
    },

    downloadReport(job) {
      window.open(`/api/exports/download/${job.id}`, "_blank");
    },

    getDateRangeText(days) {
      const ranges = { "7": "Last 7 days", "30": "Last 30 days", "90": "Last 3 months", "180": "Last 6 months", "365": "Last year", all: "All time" };
      return ranges[days] || "Custom";
    },

    getStatusClass(status) {
      return { completed: "bg-success", processing: "bg-warning text-dark", failed: "bg-danger" }[status] || "bg-secondary";
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
  },
};
</script>
