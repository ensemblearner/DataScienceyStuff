
package org.hadoop.search;

import java.util.*;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.io.Text;

public class Node {

    public static enum Status {
        NOTVISITED, START, VISITED
    };

    private final int id;
    private int distance;
    private List<Integer> edges = new ArrayList<Integer>();
    private Status status = Status.NOTVISITED;

    public Node(String str) {
        String[] map = str.split("\t");
        String key = map[0];
        String value = map[1];
        String[] tokens = value.split("\\|");
        this.id = Integer.parseInt(key);
        for (String s : tokens[0].split(",")) {
            if (s.length() > 0) {
                edges.add(Integer.parseInt(s));
            }
        }
        if (tokens[1].equals("inf")) {
            this.distance = Integer.MAX_VALUE;
        } else {
            this.distance = Integer.parseInt(tokens[1]);
        }
        this.status = Status.valueOf(tokens[2]);
    }

    public Node(int id) {
        this.id = id;
    }

    public int getId() {
        return this.id;
    }

    public int getDistance() {
        return this.distance;
    }

    public void setDistance(int distance) {
        this.distance = distance;
    }

    public Status getStatus() {
        return this.status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

    public List<Integer> getEdges() {
        return this.edges;
    }

    public void setEdges(List<Integer> edges) {
        this.edges = edges;
    }

    public Text getLine() {
        StringBuffer s = new StringBuffer();

        for (int v : edges) {
            s.append(v).append(",");
        }
        s.append("|");

        if (this.distance < Integer.MAX_VALUE) {
            s.append(this.distance).append("|");
        } else {
            s.append("inf").append("|");
        }

        s.append(status.toString());

        return new Text(s.toString());
    }

}