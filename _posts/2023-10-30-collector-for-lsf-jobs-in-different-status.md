---
layout: post
title: 一个收集LSF处于不同状态job数量的collector
date: 2023-10-30 22:25+0800
description: 
tags: lsf
giscus_comments: true
categories: icenv
---

基于 https://github.com/icinfra/lsf_exporter 提供的LSF collector的样例，以及EDACAD群友希望增加对处于不同状态的job的统计展示，这里提供一个


```go
// 作者: wanlinwang
// 日期: 2023-10-30
// 描述: 这个文件包含了Prometheus的collector实现，用于收集LSF job状态信息。


package collector

import (
	"bytes"
	"os/exec"
	"strconv"
	"strings"

	"github.com/go-kit/log"
	"github.com/prometheus/client_golang/prometheus"
)

type lsfJobCollector struct {
	RunJobs  *prometheus.Desc
	PendJobs *prometheus.Desc
	SuspJobs *prometheus.Desc
	logger   log.Logger
}

func init() {
	registerCollector("lsfjobs", defaultEnabled, NewLSFJobCollector)
}

func NewLSFJobCollector(logger log.Logger) (Collector, error) {
	return &lsfJobCollector{
		RunJobs: prometheus.NewDesc(
			prometheus.BuildFQName(namespace, "lsfjobs", "run"),
			"The total number of RUNNING jobs.",
			nil, nil,
		),
		PendJobs: prometheus.NewDesc(
			prometheus.BuildFQName(namespace, "lsfjobs", "pend"),
			"The total number of PENDING jobs.",
			nil, nil,
		),
		SuspJobs: prometheus.NewDesc(
			prometheus.BuildFQName(namespace, "lsfjobs", "susp"),
			"The total number of SUSPENDED jobs.",
			nil, nil,
		),
		logger: logger,
	}, nil
}

func (c *lsfJobCollector) Update(ch chan<- prometheus.Metric) error {
	jobStats, err := getLSFJobStats(c.logger)
	if err != nil {
		return err
	}

	ch <- prometheus.MustNewConstMetric(c.RunJobs, prometheus.GaugeValue, float64(jobStats.Run))
	ch <- prometheus.MustNewConstMetric(c.PendJobs, prometheus.GaugeValue, float64(jobStats.Pend))
	ch <- prometheus.MustNewConstMetric(c.SuspJobs, prometheus.GaugeValue, float64(jobStats.Susp))

	return nil
}

type JobStats struct {
	Run  int
	Pend int
	Susp int
}

func getLSFJobStats(logger log.Logger) (*JobStats, error) {
	cmd := exec.Command("bash", "-c", "bqueues")
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		return nil, err
	}

	lines := strings.Split(out.String(), "\n")
	totalRun, totalPend, totalSusp := 0, 0, 0

	// 从第二行开始处理，以忽略 header 行
	for i, line := range lines {
		if i == 0 {
			continue  // skip header line
		}
		fields := strings.Fields(line)
		if len(fields) >= 8 {
			run, err := strconv.Atoi(fields[9])
			if err == nil {
				totalRun += run
			}

			pend, err := strconv.Atoi(fields[8])
			if err == nil {
				totalPend += pend
			}

			susp, err := strconv.Atoi(fields[10])
			if err == nil {
				totalSusp += susp
			}
		}
	}

	return &JobStats{
		Run:  totalRun,
		Pend: totalPend,
		Susp: totalSusp,
	}, nil
}

```

参考资料

<img width="616" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/5aa1a9a1-0503-43e8-9713-fd755ecb4574">

<img width="599" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/d68b3e71-c632-448c-a423-d4e147f25afd">

https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=status-find-batch-system#bhostsbqueues9786__title__3


