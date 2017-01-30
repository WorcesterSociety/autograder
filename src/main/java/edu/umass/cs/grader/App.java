/*
 * UMass Grader
 * Copyright (C) 2017 Aaron Weiss
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
package edu.umass.cs.grader;

import com.spotify.docker.client.DefaultDockerClient;
import com.spotify.docker.client.DockerClient;
import com.spotify.docker.client.LogStream;
import com.spotify.docker.client.exceptions.DockerCertificateException;
import com.spotify.docker.client.exceptions.DockerException;
import com.spotify.docker.client.messages.ContainerConfig;
import com.spotify.docker.client.messages.ContainerCreation;
import com.spotify.docker.client.messages.ExecCreation;
import com.spotify.docker.client.messages.HostConfig;

public class App {
    public static void main(String[] args) {
        try {
            DockerClient docker = new DefaultDockerClient("unix:///var/run/docker.sock");

            HostConfig hostConfig = HostConfig.builder()
                    .appendBinds(HostConfig.Bind
                            .from(".")
                            .to("/opt/assignment")
                            .readOnly(true)
                            .build()
                    )
                    .build();

            ContainerConfig config = ContainerConfig.builder().image("python:latest")
                    .attachStdout(true).attachStderr(true)
                    .tty(true)
                    .env("PYTHONUNBUFFERED=0")
                    .cmd("python", "-u", "-c", "'print(\"Hello, World.\")'")
                    .build();

            ContainerCreation container = docker.createContainer(config);
            docker.startContainer(container.id());

//            ExecCreation exec = docker.execCreate(container.id(), new String[]{
//                    "python", "-c", "'print(\"Hello World\")'"
//            }, DockerClient.ExecCreateParam.attachStdout(true), DockerClient.ExecCreateParam.attachStderr(true));
//            LogStream stream = docker.execStart(exec.id(), DockerClient.ExecStartParameter.TTY);
            docker.waitContainer(container.id());

            String output = docker.logs(
                    container.id(), DockerClient.LogsParam.stdout(), DockerClient.LogsParam.stderr()
            ).readFully();

            System.out.println("Python Output:");
            System.out.println(output);

            docker.removeContainer(container.id());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (DockerException e) {
            e.printStackTrace();
        }
    }
}
