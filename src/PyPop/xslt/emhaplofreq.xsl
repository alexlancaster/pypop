<!--
This file is part of PyPop

  Copyright (C) 2003. The Regents of the University of California (Regents) 
  All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
-->
<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:data="any-uri">

 <!-- #################  HAPLOTYPE/LD STATISTICS ###################### --> 

 <data:haplo-fields>
  <text col="individcount">Number of individuals</text>
  <text col="uniquepheno">Unique phenotypes</text>
  <text col="uniquegeno">Unique genotypes</text>
  <text col="haplocount">Number of haplotypes</text>
  <text col="iterConverged">Number of iterations before convergence</text>
  <text col="loglikelihood-no-ld">Loglikelihood under linkage equilibrium [ln(L_0)]</text>
  <text col="loglikelihood">Loglikelihood obtained via the EM algorithm [ln(L_1)]</text>
 </data:haplo-fields>

 <xsl:template match="emhaplofreq/group"/> 
 <xsl:template match="haplostats/group"/> 

 <xsl:template match="emhaplofreq|haplostats">
  <xsl:call-template name="section">
   <xsl:with-param name="level" select="2"/>
   <xsl:with-param name="title">Haplotype / linkage disequilibrium (LD) statistics</xsl:with-param>
   <xsl:with-param name="text">
    
    <!-- first print out table of all pairwise LD (without HFs by default) -->
    <xsl:call-template name="pairwise-ld">
     <xsl:with-param name="loci" 
      select="group[@mode='all-pairwise-ld-with-permu' or 
      @mode='all-pairwise-ld-no-permu']"/>
    </xsl:call-template>

    <xsl:apply-templates select="group[@mode='LD']"/>

    <!-- now print out haplotype frequencies for those specified haplotypes -->
    <xsl:apply-templates select="group[@showHaplo='yes']"/>
  </xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <xsl:template match="group[@showHaplo='yes']">
  <xsl:call-template name="section">
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="title">Haplotype frequency est. for loci: <xsl:value-of select="@loci"/>
   </xsl:with-param>
   <xsl:with-param name="text">
    
    <xsl:for-each
     select="uniquepheno|uniquegeno|haplocount|individcount">
     <xsl:value-of
      select="document('')//data:haplo-fields/text[@col=name(current())]"/>
     <xsl:text>: </xsl:text>
     <xsl:value-of select="."/>
     <xsl:if test="@role">
      <xsl:text> (</xsl:text>
      <xsl:value-of select="@role"/>
      <xsl:text>)</xsl:text>
     </xsl:if>
     <xsl:call-template name="newline"/>
    </xsl:for-each>
    
    <xsl:choose>
     <xsl:when test="haplotypefreq/condition[@role='converged']">
      <xsl:value-of 
       select="document('')//data:haplo-fields/text[@col='loglikelihood-no-ld']"/>  
      <xsl:text>: </xsl:text>
      <xsl:value-of select="loglikelihood"/>
      <xsl:call-template name="newline"/>
      <xsl:value-of 
       select="document('')//data:haplo-fields/text[@col='loglikelihood']"/>  
      <xsl:text>: </xsl:text>
      <xsl:value-of select="haplotypefreq/loglikelihood"/>
      <xsl:call-template name="newline"/>
      <xsl:value-of 
       select="document('')//data:haplo-fields/text[@col='iterConverged']"/>  
      <xsl:text>: </xsl:text>
      <xsl:value-of select="haplotypefreq/iterConverged"/>
      <xsl:call-template name="newline"/>

      <xsl:call-template name="newline"/>

      <xsl:apply-templates select="haplotypefreq"/>
     </xsl:when>
     <xsl:otherwise>
      <xsl:text>EM algorithm failed to converge.</xsl:text>
      <xsl:call-template name="newline"/>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>


 <!-- named template to generate table of all pairwise LD statistics -->
 <xsl:template name="pairwise-ld">
  <xsl:param name="loci"/>

  <xsl:call-template name="section">
   <xsl:with-param name="title">Pairwise LD estimates</xsl:with-param>
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="text">

    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">Locus pair</xsl:with-param>
     <xsl:with-param name="length" select="15"/>
     <xsl:with-param name="type" select="'left'"/>
    </xsl:call-template>
    
    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">D</xsl:with-param>
     <xsl:with-param name="length" select="8"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>
    
    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">D'</xsl:with-param>
     <xsl:with-param name="length" select="8"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>
    
    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">Wn</xsl:with-param>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>

    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">ln(L_1)</xsl:with-param>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>

    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">ln(L_0)</xsl:with-param>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>

    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">S</xsl:with-param>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>
    
    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">ALD_1_2</xsl:with-param>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>
    
    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">ALD_2_1</xsl:with-param>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>

    <xsl:choose>
      <xsl:when test="$loci/@mode='all-pairwise-ld-with-permu'">
	<xsl:call-template name="justified-cell">
	  <xsl:with-param name="padVar">permus</xsl:with-param>
	  <xsl:with-param name="length" select="8"/>
	  <xsl:with-param name="type" select="'right'"/>
	</xsl:call-template>

	<xsl:call-template name="justified-cell">
	  <xsl:with-param name="padVar"> p-value</xsl:with-param>
	  <xsl:with-param name="length" select="9"/>
	  <xsl:with-param name="type" select="'left'"/>
	</xsl:call-template>	
      </xsl:when>
    </xsl:choose>
    
    <xsl:call-template name="newline"/>
    
    <xsl:for-each select="$loci">
     
     <xsl:if test="not(@role='no-data')">
      
      <!-- make sure convergence has happened -->
      <!--   <xsl:when test="../haplotypefreq/condition/@role='converged'"> -->
      
      <xsl:variable name="locus-pair" select="@loci"/>
      
      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar" select="$locus-pair"/>
       <xsl:with-param name="length" select="15"/>
       <xsl:with-param name="type" select="'left'"/>
      </xsl:call-template>

      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar" select="linkagediseq/summary/dsummary"/>
       <xsl:with-param name="length" select="8"/>
       <xsl:with-param name="type" select="'right'"/>
      </xsl:call-template>
      
      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar" select="linkagediseq/summary/dprime"/>
       <xsl:with-param name="length" select="8"/>
       <xsl:with-param name="type" select="'right'"/>
      </xsl:call-template>
      
      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar" select="linkagediseq/summary/wn"/>
       <xsl:with-param name="length" select="10"/>
       <xsl:with-param name="type" select="'right'"/>
      </xsl:call-template>

      <xsl:variable name="L_1" select="haplotypefreq/loglikelihood"/>
      <xsl:variable name="L_0" select="loglikelihood[@role='no-ld']"/>
      <xsl:variable name="test-stat" select="-2 * ($L_0 - $L_1)"/>
      
      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar">
	<xsl:call-template name="round-to">
	 <xsl:with-param name="node" select="$L_1"/>
	 <xsl:with-param name="places" select="2"/>
	</xsl:call-template>
       </xsl:with-param>
       <xsl:with-param name="length" select="10"/>
       <xsl:with-param name="type" select="'right'"/>
      </xsl:call-template>

      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar">
	<xsl:call-template name="round-to">
	 <xsl:with-param name="node" select="$L_0"/>
	 <xsl:with-param name="places" select="2"/>
	</xsl:call-template>
       </xsl:with-param>
       <xsl:with-param name="length" select="10"/>
       <xsl:with-param name="type" select="'right'"/>
      </xsl:call-template>

      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar">
	<xsl:call-template name="round-to">
	 <xsl:with-param name="node" select="$test-stat"/>
	 <xsl:with-param name="places" select="2"/>
	</xsl:call-template>
       </xsl:with-param>
       <xsl:with-param name="length" select="10"/>
       <xsl:with-param name="type" select="'right'"/>
      </xsl:call-template>
      
      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar" select="linkagediseq/summary/ALD_1_2"/>
       <xsl:with-param name="length" select="10"/>
       <xsl:with-param name="type" select="'right'"/>
      </xsl:call-template>

      <xsl:call-template name="justified-cell">
       <xsl:with-param name="padVar" select="linkagediseq/summary/ALD_2_1"/>
       <xsl:with-param name="length" select="10"/>
       <xsl:with-param name="type" select="'right'"/>
      </xsl:call-template>

      <xsl:choose>
	<xsl:when test="$loci/@mode='all-pairwise-ld-with-permu'">

	  <xsl:call-template name="justified-cell">
	    <xsl:with-param name="padVar">
	      <xsl:choose>
		<xsl:when test="permutationSummary/pvalue">
		  <xsl:value-of select="permutationSummary/pvalue/@totalperm"/>
		</xsl:when>
		<xsl:otherwise>-</xsl:otherwise>
	      </xsl:choose>
	    </xsl:with-param>
	    <xsl:with-param name="length" select="8"/>
	    <xsl:with-param name="type" select="'right'"/>
	  </xsl:call-template>
	  
	  <xsl:call-template name="justified-cell">
	    <xsl:with-param name="padVar">
	      <xsl:text> </xsl:text>
	      <xsl:choose>
		<xsl:when test="permutationSummary/pvalue">
		  <xsl:apply-templates select="permutationSummary/pvalue"/>
		</xsl:when>
		<xsl:otherwise>-</xsl:otherwise>
	      </xsl:choose>
	    </xsl:with-param>
	    <xsl:with-param name="length" select="8"/>
	    <xsl:with-param name="type" select="'left'"/>
	  </xsl:call-template>
	</xsl:when>
      </xsl:choose>
      
      <xsl:call-template name="newline"/>
     </xsl:if>
     
    </xsl:for-each>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>
 
 <!-- FIXME: this could be a redundant template, probably shouldn't have -->
 <!-- LD in non-all-pairwise mode -->
 <xsl:template match="group[@mode='LD']">

  <xsl:call-template name="header">
   <xsl:with-param name="title">LD est. for loci: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
  
  <xsl:call-template name="linesep-fields">
   <xsl:with-param name="nodes" select="uniquepheno|uniquegeno|haplocount|loglikelihood|individcount"/>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
  
  <xsl:call-template name="newline"/>
  
  <xsl:apply-templates select="permutationSummary"/>
  
  <xsl:call-template name="newline"/>
 </xsl:template>
 
 <!-- next two  templates trap the conditions in which no data or too -->
 <!-- many lines were presented to emhaplofreq -->
 <xsl:template match="group[@role='no-data']">
  <xsl:call-template name="section">
   <xsl:with-param name="title">No data left after filtering at: <xsl:value-of select="@loci"/>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
  </xsl:call-template>
 </xsl:template>

 <xsl:template match="group[@role='too-many-lines']">
  <xsl:call-template name="section">
   <xsl:with-param name="title">Too many rows for haplotype programme: <xsl:value-of select="@loci"/>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
  </xsl:call-template>
 </xsl:template>

 <xsl:template match="group[@role='max-allele-length-exceeded']">
  <xsl:call-template name="section">
   <xsl:with-param name="title">Allele name length exceeded maximum of <xsl:value-of select="."/> for loci <xsl:value-of select="@loci"/>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
  </xsl:call-template>
 </xsl:template>


 <!-- generate the haplotype frequency table -->
 <xsl:template match="haplotypefreq">

  <xsl:variable name="max-haplo-len"> 
   <xsl:call-template name="max-string-len">
    <xsl:with-param name="path" select="haplotype/@name"/>
   </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="extended">
   <xsl:choose>
    <xsl:when test="$max-haplo-len &lt; 20">0</xsl:when>
    <xsl:otherwise>1</xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <xsl:choose>
   <xsl:when test="condition/@role='converged'">

    <xsl:variable name="haplos-header">
     <!-- create header for table -->
     <xsl:call-template name="append-pad">
      <xsl:with-param name="padVar">haplotype</xsl:with-param>
      <xsl:with-param name="length">
       <xsl:choose>
	<xsl:when test="$extended=1">42</xsl:when>
	<xsl:otherwise>21</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>
     
     <xsl:call-template name="append-pad">
      <xsl:with-param name="padVar">frequency</xsl:with-param>
      <xsl:with-param name="length">9</xsl:with-param>
     </xsl:call-template>
     
     <xsl:call-template name="append-pad">
      <xsl:with-param name="padVar"># copies</xsl:with-param>
      <xsl:with-param name="length">8</xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="newline"/>
    </xsl:variable>

    <xsl:variable name="haplos-by-name">

     <xsl:call-template name="append-pad">
      <xsl:with-param name="padVar">Haplotypes sorted by name</xsl:with-param>
      <xsl:with-param name="length">38</xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="newline"/>

     <xsl:value-of select="$haplos-header"/>
     
     <!-- loop through each haplotype by name -->
     <xsl:for-each select="haplotype">
      <xsl:sort select="@name" data-type="text" order="ascending"/>
       
      <xsl:call-template name="append-pad">
       <xsl:with-param name="padVar" select="@name"/>
       <xsl:with-param name="length">
       <xsl:choose>
	<xsl:when test="$extended=1">42</xsl:when>
	<xsl:otherwise>21</xsl:otherwise>
       </xsl:choose>
       </xsl:with-param>
      </xsl:call-template>
      
      <xsl:call-template name="append-pad">
	<xsl:with-param name="padVar">
	<xsl:call-template name="round-to">
	 <xsl:with-param name="node" select="frequency"/>
	 <xsl:with-param name="places" select="5"/>
	</xsl:call-template>
	</xsl:with-param>
       <xsl:with-param name="length">9</xsl:with-param>
      </xsl:call-template>
      
      <xsl:call-template name="append-pad">
       <xsl:with-param name="padVar" select="numCopies"/>
       <xsl:with-param name="length">8</xsl:with-param>
      </xsl:call-template>
      
      <xsl:call-template name="newline"/>
     </xsl:for-each>
    </xsl:variable>

    <xsl:variable name="haplos-by-freq">

     <xsl:call-template name="append-pad">
      <xsl:with-param name="padVar">Haplotypes sorted by frequency</xsl:with-param>
      <xsl:with-param name="length">38</xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="newline"/>

     <xsl:value-of select="$haplos-header"/>

     <!-- loop through each haplotype by frequency -->
     <xsl:for-each select="haplotype">
      <xsl:sort select="frequency" data-type="number" order="descending"/>
      
      <xsl:call-template name="append-pad">
       <xsl:with-param name="padVar" select="@name"/>
       <xsl:with-param name="length">
	<xsl:choose>
	 <xsl:when test="$extended=1">42</xsl:when>
	 <xsl:otherwise>21</xsl:otherwise>
	</xsl:choose>
       </xsl:with-param>
      </xsl:call-template>
      
      <xsl:call-template name="append-pad">
	<xsl:with-param name="padVar">
	  <xsl:call-template name="round-to">
	    <xsl:with-param name="node" select="frequency"/>
	    <xsl:with-param name="places" select="5"/>
	  </xsl:call-template>
	</xsl:with-param>
       <xsl:with-param name="length">9</xsl:with-param>
      </xsl:call-template>
      
      <xsl:call-template name="append-pad">
       <xsl:with-param name="padVar" select="numCopies"/>
       <xsl:with-param name="length">8</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="newline"/>
     </xsl:for-each>
    </xsl:variable>

    <xsl:choose>
     <xsl:when test="$extended=1">
      <xsl:value-of select="$haplos-by-freq"/>
      <xsl:call-template name="newline"/>
      <xsl:value-of select="$haplos-by-name"/>
     </xsl:when>

     <xsl:otherwise>
      <xsl:call-template name="paste-columns">
       <xsl:with-param name="col1" select="$haplos-by-name"/>
       <xsl:with-param name="col2" select="$haplos-by-freq"/>
       <xsl:with-param name="delim" select="'| '"/>
      </xsl:call-template>
      
     </xsl:otherwise>
    </xsl:choose>

   </xsl:when>

   <xsl:when test="condition/@role='loglike-failed-converge'">
    <xsl:text>Log likelihood failed to converge in specified number of iterations.
    </xsl:text>
   </xsl:when>

   <xsl:otherwise>
    <xsl:text>Unhandled 'role': </xsl:text> <xsl:value-of
    select="condition/@role"/> 

    <xsl:text>' Please implement.</xsl:text>
   </xsl:otherwise>

  </xsl:choose>

 </xsl:template>

 <!-- FIXME: LD stats in non pairwise mode, this handles case when   -->
 <!-- there are summary stats for more than two loci, do we need to  -->
 <!-- handle this case at all?                                       -->
 <xsl:template match="linkagediseq">

  <xsl:choose>
   <xsl:when test="../haplotypefreq/condition/@role='converged'">    
    <xsl:for-each select="summary">
     <xsl:text>LD summary statistics between: </xsl:text>
     <xsl:variable name="loci" select="../../@loci"/>
     
     <xsl:call-template name="get-nth-element">
      <xsl:with-param name="delim">:</xsl:with-param>
      <xsl:with-param name="str" select="$loci"/>
      <xsl:with-param name="n" select="@first"/>
     </xsl:call-template>
     
     <xsl:text> and </xsl:text>
     
     <xsl:call-template name="get-nth-element">
      <xsl:with-param name="delim">:</xsl:with-param>
      <xsl:with-param name="str" select="$loci"/>
      <xsl:with-param name="n" select="@second"/>
     </xsl:call-template>
     
     <xsl:call-template name="newline"/>
     
     <xsl:call-template name="linesep-fields">
      <xsl:with-param name="nodes" select="dprime|wn|q/chisq|q/dof"/>
     </xsl:call-template>
     
    </xsl:for-each>
   
   </xsl:when>  

   <xsl:when test="../haplotypefreq/condition/@role='loglike-failed-converge'">
    <xsl:text>Log likelihood failed to converge: don't calculate any LD stats.</xsl:text>

    <xsl:call-template name="newline"/>
   </xsl:when>

   <xsl:otherwise>
    <xsl:text>Unhandled 'role': Please implement!</xsl:text>

    <xsl:call-template name="newline"/>
   </xsl:otherwise>

  </xsl:choose>

  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- ################# END  HAPLOTYPE/LD STATISTICS ################### --> 

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 
