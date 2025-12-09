import React, { useState } from 'react';
import * as XLSX from 'xlsx';
import { Download } from 'lucide-react';

const ProjectGanttChart = () => {
  const [downloading, setDownloading] = useState(false);

  const projectData = [
    // Initiation Phase
    { kode: '1.1', aktivitas: 'Kick-off pertama proyek', durasi: '1 hari', predecessor: '-', tipe: '-', keterangan: 'Kick-off meeting membahas proyek', startDay: 0, durationDays: 1 },
    { kode: '1.2', aktivitas: 'Identifikasi stakeholder', durasi: '1 hari', predecessor: '1.1', tipe: 'SS', keterangan: 'Dumulai dengan mencari setelah kick-off', startDay: 0, durationDays: 1 },
    { kode: '1.3', aktivitas: 'Pengumpulan data proses bisnis', durasi: '2 hari', predecessor: '1.2', tipe: 'FS', keterangan: 'Setelah stakeholder ditemukan, data dikumpulkan', startDay: 1, durationDays: 2 },
    
    // Planning Phase
    { kode: '2.1', aktivitas: 'Penyusunan scope statement', durasi: '1 hari', predecessor: '1.3', tipe: 'FS', keterangan: 'Setelah data terkumpul', startDay: 3, durationDays: 1 },
    { kode: '2.2', aktivitas: 'Penyusunan WBS', durasi: '1 hari', predecessor: '2.1', tipe: 'FS', keterangan: 'Setelah scope final', startDay: 4, durationDays: 1 },
    { kode: '2.3', aktivitas: 'Penyusunan Activity List & Cost Effort', durasi: '2 hari', predecessor: '2.2', tipe: 'SS', keterangan: 'Setelah WBS', startDay: 4, durationDays: 2 },
    { kode: '2.4', aktivitas: 'Penyusunan network', durasi: '1 hari', predecessor: '2.2', tipe: 'SS', keterangan: 'Setelah WBS dan setelah List', startDay: 4, durationDays: 1 },
    { kode: '2.5', aktivitas: 'Penyusunan Risk Plan', durasi: '1 hari', predecessor: '2.3', tipe: 'FS', keterangan: 'Setelah semua sudah didefinisikan', startDay: 6, durationDays: 1 },
    
    // Execution Phase - Design
    { kode: '3.1', aktivitas: 'Perancangan database aplikasi', durasi: '2 hari', predecessor: '2.5', tipe: 'FS', keterangan: 'Desain setelah Risk Plan', startDay: 7, durationDays: 2 },
    { kode: '3.2', aktivitas: 'Perancangan database', durasi: '2 hari', predecessor: '3.1', tipe: 'SS', keterangan: 'Paralel dengan 3.1', startDay: 7, durationDays: 2 },
    { kode: '3.3', aktivitas: 'Desain UI/UX', durasi: '2 hari', predecessor: '3.1', tipe: 'SS', keterangan: 'Paralel dengan 3.1', startDay: 7, durationDays: 2 },
    
    // Execution Phase - Development
    { kode: '4.1', aktivitas: 'Modul pembuatan master', durasi: '3 hari', predecessor: '3.2', tipe: 'FS', keterangan: 'Bumb dengan step sebelum', startDay: 9, durationDays: 3 },
    { kode: '4.2', aktivitas: 'Modul pembuatan & approval transaksi', durasi: '3 hari', predecessor: '4.1', tipe: 'SS', keterangan: 'Dimulai setelah modul transaksi', startDay: 9, durationDays: 3 },
    { kode: '4.3', aktivitas: 'Modul keuangan dan pinjaman', durasi: '3 hari', predecessor: '4.2', tipe: 'SS', keterangan: 'Pembuatan modul dari modul sebelumnya', startDay: 9, durationDays: 3 },
    { kode: '4.4', aktivitas: 'Modul notifikasi', durasi: '2 hari', predecessor: '4.3', tipe: 'SS', keterangan: 'Setelah dashboard', startDay: 9, durationDays: 2 },
    { kode: '4.5', aktivitas: 'Modul upload laporan tahunan', durasi: '3 hari', predecessor: '4.3', tipe: 'SS', keterangan: 'Semua modul selesai', startDay: 9, durationDays: 3 },
    
    // Monitoring Phase
    { kode: '5', aktivitas: 'Monitoring', durasi: '3 hari', predecessor: '3.4, 4.5', tipe: 'FS', keterangan: 'Semua modul selesai', startDay: 12, durationDays: 3 },
    
    // Testing Phase
    { kode: '5.1', aktivitas: 'Unit Testing', durasi: '2 hari', predecessor: '5', tipe: 'SS', keterangan: 'Paralel per modul', startDay: 12, durationDays: 2 },
    { kode: '5.2', aktivitas: 'Integration Testing', durasi: '2 hari', predecessor: '5.1', tipe: 'FS', keterangan: 'Setelah unit testing selesai', startDay: 14, durationDays: 2 },
    { kode: '5.3', aktivitas: 'UAT', durasi: '2 hari', predecessor: '5.2', tipe: 'FS', keterangan: 'UAT', startDay: 16, durationDays: 2 },
    
    // Closing Phase
    { kode: '6.1', aktivitas: 'Deployment excel server', durasi: '1 hari', predecessor: '5.3', tipe: 'FS', keterangan: 'Setelah UAT', startDay: 18, durationDays: 1 },
    { kode: '6.2', aktivitas: 'Konfigurasi hosting & server', durasi: '1 hari', predecessor: '6.1', tipe: 'FS', keterangan: 'Final server', startDay: 19, durationDays: 1 },
    
    // Documentation Phase
    { kode: '7.1', aktivitas: 'User manual', durasi: '2 hari', predecessor: '6.2', tipe: 'SS', keterangan: 'Paralel deployment', startDay: 19, durationDays: 2 },
    { kode: '7.2', aktivitas: 'Final review', durasi: '1 hari', predecessor: '7.1', tipe: 'FS', keterangan: 'Setelah review', startDay: 21, durationDays: 1 },
    { kode: '7.3', aktivitas: 'Laporan akhir', durasi: '1 hari', predecessor: '7.2', tipe: 'FS', keterangan: 'Laporan proyek', startDay: 22, durationDays: 1 }
  ];

  const dateColumns = Array.from({ length: 24 }, (_, i) => {
    const startDate = new Date(2023, 10, 25); // Nov 25, 2023
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);
    const month = date.toLocaleString('en', { month: 'short' });
    const day = date.getDate();
    return `${month} ${day}`;
  });

  const generateExcel = () => {
    setDownloading(true);
    
    try {
      const wb = XLSX.utils.book_new();
      
      const headers = [
        'Kode', 'Aktivitas', 'Durasi', 'Predecessor', 'Tipe', 'Keterangan',
        ...dateColumns
      ];
      
      const wsData = [headers];
      
      projectData.forEach(item => {
        const row = [
          item.kode,
          item.aktivitas,
          item.durasi,
          item.predecessor,
          item.tipe,
          item.keterangan,
          ...Array(24).fill('')
        ];
        
        // Fill Gantt bars in Excel with "■" symbol
        for (let i = 0; i < item.durationDays; i++) {
          const colIndex = item.startDay + i;
          if (colIndex < 24) {
            row[6 + colIndex] = '■';
          }
        }
        
        wsData.push(row);
      });
      
      const ws = XLSX.utils.aoa_to_sheet(wsData);
      
      ws['!cols'] = [
        { wch: 8 },  // Kode
        { wch: 35 }, // Aktivitas
        { wch: 10 }, // Durasi
        { wch: 12 }, // Predecessor
        { wch: 8 },  // Tipe
        { wch: 40 }, // Keterangan
        ...Array(24).fill({ wch: 5 })
      ];
      
      XLSX.utils.book_append_sheet(wb, ws, 'Project Schedule');
      XLSX.writeFile(wb, 'Project_Gantt_Chart_Complete.xlsx');
      
      setTimeout(() => setDownloading(false), 1000);
    } catch (error) {
      console.error('Error generating Excel:', error);
      setDownloading(false);
    }
  };

  const getPhaseColor = (kode) => {
    if (kode.startsWith('1.')) return 'bg-purple-500';
    if (kode.startsWith('2.')) return 'bg-blue-500';
    if (kode.startsWith('3.')) return 'bg-green-500';
    if (kode.startsWith('4.')) return 'bg-yellow-500';
    if (kode.startsWith('5')) return 'bg-orange-500';
    if (kode.startsWith('6.')) return 'bg-red-500';
    if (kode.startsWith('7.')) return 'bg-pink-500';
    return 'bg-gray-500';
  };

  return (
    <div className="w-full min-h-screen bg-gray-50 p-6">
      <div className="max-w-full mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-gray-800">Project Gantt Chart - Complete</h1>
            <button
              onClick={generateExcel}
              disabled={downloading}
              className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:bg-gray-400"
            >
              <Download size={20} />
              {downloading ? 'Generating...' : 'Download Excel'}
            </button>
          </div>
          <p className="text-gray-600 mb-4">
            Data lengkap dari Initiation hingga Documentation phase dengan timeline akurat sesuai predecessor dan durasi.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-xs border-collapse">
              <thead className="bg-gray-800 text-white">
                <tr>
                  <th className="px-2 py-2 text-left font-semibold border border-gray-600 w-16">Kode</th>
                  <th className="px-2 py-2 text-left font-semibold border border-gray-600 w-64">Aktivitas</th>
                  <th className="px-2 py-2 text-center font-semibold border border-gray-600 w-20">Durasi</th>
                  <th className="px-2 py-2 text-center font-semibold border border-gray-600 w-24">Predecessor</th>
                  <th className="px-2 py-2 text-center font-semibold border border-gray-600 w-12">Tipe</th>
                  <th className="px-2 py-2 text-left font-semibold border border-gray-600 w-72">Keterangan</th>
                  {dateColumns.slice(0, 16).map((date, i) => (
                    <th key={i} className="px-1 py-2 text-center font-semibold border border-gray-600 w-10 text-xs bg-gray-700">
                      {date}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white">
                {projectData.map((item, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    <td className="px-2 py-2 border border-gray-300 text-xs font-semibold">{item.kode}</td>
                    <td className="px-2 py-2 border border-gray-300 text-xs">{item.aktivitas}</td>
                    <td className="px-2 py-2 border border-gray-300 text-center text-xs">{item.durasi}</td>
                    <td className="px-2 py-2 border border-gray-300 text-center text-xs">{item.predecessor}</td>
                    <td className="px-2 py-2 border border-gray-300 text-center text-xs">{item.tipe}</td>
                    <td className="px-2 py-2 border border-gray-300 text-xs">{item.keterangan}</td>
                    {dateColumns.slice(0, 16).map((_, colIndex) => {
                      const isInRange = colIndex >= item.startDay && colIndex < item.startDay + item.durationDays;
                      const isStart = colIndex === item.startDay;
                      const isEnd = colIndex === item.startDay + item.durationDays - 1;
                      
                      return (
                        <td key={colIndex} className="border border-gray-300 p-0 relative h-8">
                          {isInRange && (
                            <div className="absolute inset-0 flex items-center justify-center">
                              <div 
                                className={`h-5 ${getPhaseColor(item.kode)} ${isStart ? 'rounded-l' : ''} ${isEnd ? 'rounded-r' : ''}`}
                                style={{ width: '100%' }}
                              ></div>
                            </div>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-2 gap-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">📊 Phase Legend:</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li className="flex items-center gap-2"><span className="w-4 h-4 bg-purple-500 rounded"></span> 1.x - Initiation</li>
              <li className="flex items-center gap-2"><span className="w-4 h-4 bg-blue-500 rounded"></span> 2.x - Planning</li>
              <li className="flex items-center gap-2"><span className="w-4 h-4 bg-green-500 rounded"></span> 3.x - Execution (Design)</li>
              <li className="flex items-center gap-2"><span className="w-4 h-4 bg-yellow-500 rounded"></span> 4.x - Execution (Development)</li>
            </ul>
          </div>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 className="font-semibold text-green-900 mb-2">✅ Fitur:</h3>
            <ul className="text-sm text-green-800 space-y-1">
              <li className="flex items-center gap-2"><span className="w-4 h-4 bg-orange-500 rounded"></span> 5.x - Monitoring & Testing</li>
              <li className="flex items-center gap-2"><span className="w-4 h-4 bg-red-500 rounded"></span> 6.x - Closing</li>
              <li className="flex items-center gap-2"><span className="w-4 h-4 bg-pink-500 rounded"></span> 7.x - Documentation</li>
              <li>• Timeline disesuaikan dengan predecessor</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectGanttChart;