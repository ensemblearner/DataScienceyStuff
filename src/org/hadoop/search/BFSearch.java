package org.hadoop.search;

import java.io.IOException;
import java.util.List;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/* BFS MapReduce Algorithm
 * From book : Data-Intensive Text Processing with MapReduce: Jimmy Lin and Chris Dyer
 * class Mapper
		method Map(nid n, node N )
		d ← N.Distance
		Emit(nid n, N )
		Pass along graph structure
		for all nodeid m ∈ N.AdjacencyList do
			Emit(nid m, d + 1)
			Emit distances to reachable nodes
	class Reducer
		method Reduce(nid m, [d1 , d2 , . . .])
		dmin ← ∞
		M ←∅
		for all d ∈ counts [d1 , d2 , . . .] do
			if IsNode(d) then
				M ←d
			else if d < dmin then
				dmin ← d
			M.Distance ← dmin
			Emit(nid m, node M )
 */
public class BFSearch extends Configured implements Tool {

    public static final Log LOG = LogFactory.getLog("org.hadoop.search.BFSearch");
    public static class MapClass extends  Mapper<LongWritable, Text, IntWritable, Text> {
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            Node node = new Node(value.toString());
            if (node.getStatus() == Node.Status.START) {
                for (int v : node.getEdges()) {
                    Node vnode = new Node(v);
                    vnode.setDistance(node.getDistance() + 1);
                    vnode.setStatus(Node.Status.START);
                    context.write(new IntWritable(vnode.getId()), vnode.getLine());
                }
                node.setStatus(Node.Status.VISITED);
            }
              context.write(new IntWritable(node.getId()), node.getLine());

        }
    }


    public static class ReduceClass extends Reducer<IntWritable, Text, IntWritable, Text> {
        
    	public void reduce(IntWritable key, Iterable<Text> values,
                           Context context) throws IOException, InterruptedException {
            List<Integer> edges = null;
            int distance = Integer.MAX_VALUE;
            Node.Status status = Node.Status.VISITED;
            for (Text value: values){
                Node e = new Node(key.get() + "\t" + value.toString());
                if (e.getEdges().size() > 0) {
                    edges = e.getEdges();
                }
                if (e.getDistance() < distance) {
                    distance = e.getDistance();
                }
                if (e.getStatus().ordinal() > status.ordinal()) {
                    status = e.getStatus();
                }

            }

            Node n = new Node(key.get());
            n.setDistance(distance);
            n.setEdges(edges);
            n.setStatus(status);
            context.write(key, new Text(n.getLine()));

        }
    }

    public static void main(String[] args) throws Exception {

        int res = ToolRunner.run(new Configuration(), new BFSearch(), args);
        System.exit(res);
    }
    

    public int run(String[] args) throws Exception {

        int maxIter = 4;
        int res = 0;
        String input = args[0];
        String foutput = args[1];
        for (int curIter = 0; curIter < maxIter; curIter++){
            if (curIter != 0)
                input = foutput +"-" + curIter; 
            String output = foutput+ "-" + (curIter + 1);
            System.out.println("iteration number " + curIter);
            System.out.println("Reading from: " + input);
            System.out.println("Writing to : " + output);
            System.out.println("=========================");
            Configuration configuration = getConf();
            Job job = new Job(configuration, "BFSearch");
            job.setJarByClass(BFSearch.class);
            job.setMapperClass(MapClass.class);
            job.setReducerClass(ReduceClass.class);
            job.setOutputKeyClass(IntWritable.class);
            job.setOutputValueClass(Text.class);
            FileInputFormat.addInputPath(job,new Path(input));
            FileOutputFormat.setOutputPath(job, new Path(output));
            res = job.waitForCompletion(true) ? 0 : -1;
            
        }

        return res;
    }

  

}