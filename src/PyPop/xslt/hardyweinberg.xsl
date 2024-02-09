<!--
This file is part of PyPop

  Copyright (C) 2003-2006. 
  The Regents of the University of California (Regents) 
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
 xmlns:exslt="http://exslt.org/common"
 extension-element-prefixes="exslt"
 xmlns:data="any-uri">

 <xsl:param name="indiv-geno-pval-cutoff" select="0.05"/>

 <xsl:param name="new-hardyweinberg-format" select="0"/>

 <!-- boiler-plate text that we may want to re-use -->
 <data:hardyweinberg-col-headers>
  <text col="observed">Observed</text>
  <text col="expected">Expected</text>
  <text col="chisq">Chi-square</text>
  <text col="chisqdf" colwidth="6">DoF</text>
  <text col="pvalue" justify="left">p-value</text>
 </data:hardyweinberg-col-headers>

 <data:hardyweinberg-guo-thompson>
  <text col="dememorizationSteps">Dememorization steps</text>
  <text col="samplingNum">Number of Markov chain samples</text>
  <text col="samplingSize">Markov chain sample size</text>
  <text col="steps">Steps in Monte-Carlo randomization</text>
  <text col="pvalue">p-value</text>
  <text col="stderr">Std. error</text>
 </data:hardyweinberg-guo-thompson>

 <data:hardyweinberg-guo-thompson-arlequin>
  <text col="obs-hetero">Observed heterozygosity</text>
  <text col="exp-hetero">Expected heterozygosity</text>
  <text col="steps">Steps in Markov chain</text>
  <text col="pvalue">p-value</text>
  <text col="stddev">Std. deviation</text>
 </data:hardyweinberg-guo-thompson-arlequin>

 <xsl:variable name="hw-col-headers" 
  select="document('')//data:hardyweinberg-col-headers/text"/>

 <xsl:variable name="hw-guo-thompson" 
  select="document('')//data:hardyweinberg-guo-thompson/text"/>

 <xsl:variable name="hw-guo-thompson-arlequin" 
  select="document('')//data:hardyweinberg-guo-thompson-arlequin/text"/>

 <!-- ################  HARDY-WEINBERG STATISTICS ###################### --> 

 <!-- find the maximum possible genotype length across the whole input file 
      use this as the column width -->
 <xsl:variable name="hardyweinberg-first-col-width">
   <xsl:variable name="max-row-len">
     <xsl:call-template name="max-string-len">
       <xsl:with-param name="path" select="//genotypetable/genotype/@row"/>
     </xsl:call-template>
   </xsl:variable>
   <xsl:variable name="max-col-len">
     <xsl:call-template name="max-string-len">
       <xsl:with-param name="path" select="//genotypetable/genotype/@col"/>
     </xsl:call-template>
   </xsl:variable>
   <xsl:choose>
     <xsl:when test="$max-row-len + $max-col-len + 1 &lt; $hardyweinberg-col-width">
       <xsl:value-of select="$hardyweinberg-col-width"/>
     </xsl:when>
     <xsl:otherwise>
       <xsl:value-of select="$max-row-len + $max-col-len + 1"/>
     </xsl:otherwise>
   </xsl:choose>
 </xsl:variable>

<xsl:template match="hardyweinberg">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">
      <xsl:text>HardyWeinberg</xsl:text>
      <xsl:choose>
       <xsl:when test="@allelelump=0 or not(@allelelump)"></xsl:when>
       <xsl:otherwise>
	<xsl:text> (lump alleles &lt;= </xsl:text>
	<xsl:value-of select="@allelelump"/>
	<xsl:text>)</xsl:text>
       </xsl:otherwise>
      </xsl:choose>
     </xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="text">

     <!-- do genotype table -->
    <xsl:apply-templates select="genotypetable"/>
    
    <xsl:call-template name="newline"/>

    <!-- indent first line of table -->
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
    </xsl:call-template>
    
    <!-- print header for the individual stats -->
    <xsl:for-each select="$hw-col-headers">
     <xsl:variable name="width">
      <xsl:choose>
       <xsl:when test="@colwidth">
	<xsl:value-of select="@colwidth"/>
       </xsl:when>
       <xsl:otherwise> 
	<xsl:value-of select="$hardyweinberg-col-width"/>
       </xsl:otherwise>
      </xsl:choose>
     </xsl:variable>
     <xsl:choose>
      <xsl:when test="@justify='left'">
       <xsl:text> </xsl:text>
       <xsl:call-template name="append-pad">
	<xsl:with-param name="padVar">
	 <xsl:text>  </xsl:text>
	 <xsl:value-of select="."/>
	</xsl:with-param>
	<xsl:with-param name="length" select="$width"/>
       </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
       <xsl:call-template name="prepend-pad">
	<xsl:with-param name="padVar" select="."/>
	<xsl:with-param name="length" select="$width"/>
       </xsl:call-template>
      </xsl:otherwise>
     </xsl:choose>
    </xsl:for-each>
    
    <!-- separator -->
    <xsl:call-template name="newline"/>
    <xsl:call-template name="separator"/>
    <xsl:call-template name="newline"/>
    
    <!-- no do individual stats for each class -->
    <xsl:apply-templates select="common"/>
    <xsl:apply-templates select="lumped"/>
    <xsl:apply-templates select="commonpluslumped"/>
    <xsl:apply-templates select="heterozygotes|homozygotes"/>
    
    <!-- do stats for all the heterozygotes and genotypes -->
    <xsl:apply-templates select="heterozygotesByAllele"/>
    
    <xsl:apply-templates select="genotypetable" mode="genotypesByGenotype"/>
 
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>
 
 <!-- template to generate the (padded) cell ;-) -->
 <!-- this also handles the case when there is no tag because it -->
 <!-- will simply return a white-space padded cell of the right length -->
 <xsl:template name="hardyweinberg-gen-cell">
  <xsl:param name="node" select="."/>
  <xsl:param name="width" select="$hardyweinberg-col-width"/>

  <!-- some columns may be left-justified, set this param to '0' if desired -->
  <xsl:param name="prepend" select="1"/>
  
  <xsl:choose>
   <xsl:when test="$prepend=1">
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="padVar" select="$node"/>
     <xsl:with-param name="length" select="$width"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
    <!-- make sure there is at least two initial space -->
    <!-- FIXME: this entire table generation system is getting way too -->
    <!-- kludgy, need to replace the entire system, with a clean, generic --> 
    <!-- system real soon now(TM) -->
    <xsl:text>  </xsl:text>
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="$node"/>
     <xsl:with-param name="length" select="$width"/>
    </xsl:call-template>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <!-- template to generate the row -->
 <xsl:template name="hardyweinberg-gen-row">
  
  <!-- create variables from the contents of the cells  -->
  <xsl:variable name="observed">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node">
     <xsl:apply-templates select="observed"/>
    </xsl:with-param>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="expected">
   <!-- for this column only, round the expected to 2 decimal places -->
   <xsl:variable name="expected-rounded">
    <xsl:call-template name="round-to">
     <xsl:with-param name="node">
      <xsl:apply-templates select="expected"/>
     </xsl:with-param>
     <xsl:with-param name="places" select="2"/>
    </xsl:call-template>
   </xsl:variable>
   <!-- then pass this new value to the generate the table cell -->
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="$expected-rounded"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="chisq">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node">
     <xsl:call-template name="round-to">
      <xsl:with-param name="node" select="chisq"/>
      <xsl:with-param name="places" select="2"/>
     </xsl:call-template>
    </xsl:with-param>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="pvalue">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node">
       <xsl:apply-templates select="pvalue"/>
    </xsl:with-param>
    <xsl:with-param name="prepend" select="0"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="chisqdf">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="chisqdf"/>
    <xsl:with-param name="width" 
     select="$hw-col-headers[@col='chisqdf']/@colwidth"/>
   </xsl:call-template>
  </xsl:variable>

  <!-- concatenate all the cells -->
  <xsl:value-of select="concat($observed,$expected,$chisq,$chisqdf,$pvalue)"/>

 </xsl:template>

 <!-- match template for observed and expected values -->
 <xsl:template match="observed|expected">
  <xsl:choose>
   <!-- if in the context of common, lumped or commonpluslumped
   doesn't make sense to output these values -->
   <xsl:when test="parent::common or parent::lumped or parent::commonpluslumped">
    <xsl:text>N/A</xsl:text>
   </xsl:when>
   <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <!-- print out overall HW stats  -->
 <xsl:template match="common|lumped|commonpluslumped|heterozygotes|homozygotes">

  <xsl:variable name="type">
   <xsl:choose>
    <xsl:when test="name(.)='homozygotes'">All homozygotes</xsl:when>
    <xsl:when test="name(.)='heterozygotes'">All heterozygotes</xsl:when>
    <xsl:when test="name(.)='common'">Common</xsl:when>
    <xsl:when test="name(.)='commonpluslumped'">Common + lumped</xsl:when>
    <xsl:when test="name(.)='lumped'">Lumped genotypes</xsl:when>
    <xsl:otherwise>
     <xsl:message terminate="yes">Should always match something</xsl:message>
    </xsl:otherwise>
   </xsl:choose>
  </xsl:variable>
  
  
  <!-- indent table -->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
   <xsl:with-param name="padVar" select="$type"/>
  </xsl:call-template>
  
  <xsl:choose>
   
   <xsl:when test="*">
    <!-- when the tag has content generate the row -->
    <xsl:call-template name="hardyweinberg-gen-row"/>
   </xsl:when>

   <!-- if the tag does not have content, generate a diagnostic message -->
   <!-- based on the 'role' attribute -->
   <xsl:when test=".=''">

    <!-- make an extra space, for case when following text is flush left -->
    <xsl:text> </xsl:text>
  
    <xsl:choose>
     <xsl:when test="@role='too-many-parameters'">
      <xsl:text>Too many parameters for chi-square test.</xsl:text>
     </xsl:when>
     <xsl:when test="@role='no-common-genotypes'">
      <xsl:text>No commmon genotypes; chi-square cannot be calculated</xsl:text>
     </xsl:when>
     <xsl:when test="@role='no-rare-genotypes'">
      <xsl:text>No rare genotypes observed.</xsl:text>
     </xsl:when>
     <xsl:when test="@role='too-few-expected'">
      <xsl:text>
       The total number of expected genotypes is less than </xsl:text><xsl:value-of
       select="../lumpBelow"/>
     </xsl:when>
     <xsl:when test="@role='not-calculated'">
      <xsl:text>Value not calculated.</xsl:text>
     </xsl:when>
     <xsl:when test="@role='huh'">
      <xsl:text>Unhandled logical path through Hardy-Weinberg.</xsl:text>
     </xsl:when>
     <xsl:otherwise>
      <xsl:text>Condition: </xsl:text><xsl:value-of
       select="@role"/><xsl:text> not recognized.</xsl:text>
     </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="newline"/>
   </xsl:when>

   <!-- an "assert" message to test XSLT is working -->
   <xsl:otherwise>
    <xsl:message>Error! Output XML condition not covered!</xsl:message>
   </xsl:otherwise>
  </xsl:choose>
  <xsl:call-template name="newline"/>

  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- print out info on heterozygotes and genotypes -->
 <xsl:template match="heterozygotesByAllele">
  <xsl:text>Common heterozygotes by allele</xsl:text>
  <xsl:call-template name="newline"/>
  <xsl:for-each select="allele">
   
   <!-- sort by allele name -->
   <xsl:sort select="@name" data-type="text"/>
   <!-- indent table with name of the allele -->
   <xsl:call-template name="append-pad">
    <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
    <xsl:with-param name="padVar" select="@name"/>
   </xsl:call-template>
   <!-- generate the row -->
   <xsl:call-template name="hardyweinberg-gen-row"/>
   <xsl:call-template name="newline"/>
  </xsl:for-each>  

  <xsl:call-template name="newline"/>
  
  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- format genotype table for HW -->
 <xsl:template match="genotypetable" mode="genotypesByGenotype">
  <xsl:text>Common genotypes</xsl:text>
  <xsl:call-template name="newline"/>

  <xsl:for-each select="genotype[not(chisq/@role='not-calculated')]">  
   <xsl:sort select="@col" data-type="text"/>
   <!-- generate genotype name -->
   <xsl:variable name="name">
    <xsl:value-of select="@col"/><xsl:value-of select="$GL-unphased-genotype-separator"/><xsl:value-of select="@row"/> 
   </xsl:variable>

  <!-- indent table with name of the genotype -->
   <xsl:call-template name="append-pad">
    <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
    <xsl:with-param name="padVar" select="$name"/>
   </xsl:call-template>
   <!-- generate the row -->
   <xsl:call-template name="hardyweinberg-gen-row"/>
   <xsl:call-template name="newline"/>
  </xsl:for-each>

  <!-- generate totals at end of table -->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
   <xsl:with-param name="padVar" select="'Total'"/>
  </xsl:call-template>

  <xsl:call-template name="hardyweinberg-gen-cell">
   <xsl:with-param name="node" select="sum(genotype[not(chisq/@role='not-calculated')]/observed)"/>
  </xsl:call-template>
  <xsl:call-template name="hardyweinberg-gen-cell">
   <xsl:with-param name="node">
    <xsl:call-template name="round-to">
     <xsl:with-param name="node"
     select="sum(genotype[not(chisq/@role='not-calculated')]/expected)"/>
     <xsl:with-param name="places" select="2"/>
    </xsl:call-template>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- format genotype table for HW -->
 <xsl:template match="genotypetable">

  <xsl:text>Table of genotypes, format of each cell is: observed/expected.</xsl:text>
  <xsl:call-template name="newline"/>

  <xsl:variable name="unique-cols-nodes">
   <xsl:for-each select="genotype">
    <xsl:if test="not(@col = preceding-sibling::genotype/@col)">
     <unique><xsl:value-of select="@col"/></unique>
       </xsl:if>
   </xsl:for-each>
  </xsl:variable>
  
  <xsl:variable name="unique-cols-new"
   select="exslt:node-set($unique-cols-nodes)/unique"/>

  <!-- old style: get the unique list of column (allele) names -->
  <!-- from <allelecount> section -->
 
  <xsl:variable name="unique-cols-old"
   select="../../allelecounts/allele/@name"/> 

  <xsl:variable name="unique-cols" 
   select="$unique-cols-new[$new-hardyweinberg-format=1] | 
   $unique-cols-old[$new-hardyweinberg-format=0]"/>

  <!-- save the current node -->
  <xsl:variable name="curr-node" select="."/>

  <xsl:variable name="row-len-max">
   <xsl:call-template name="max-string-len">
    <xsl:with-param name="path" select="genotype/@row"/>
   </xsl:call-template>
  </xsl:variable>

  <!-- find the longest observed value -->
  <xsl:variable name="observed-max">
   <xsl:call-template name="max-string-len">
    <xsl:with-param name="path" select="genotype/observed"/>
   </xsl:call-template>
  </xsl:variable>

  <!-- calculate the  width required for each cell, this twice the maximum -->
  <!-- length of the "observed" cell 'XXX'  plus a space for scientific notation in expected -->
  <!-- plus space needed for chars  -->
  <!-- e.g.:  XXX/XXX.0 and a padding space  -->
  <!-- FIXME: this is a big kludgy, really should also compute the expected-max including sci notation -->
  <xsl:variable name="cell-width-max" select="$observed-max * 2 + 1 + 4"/>

  <!-- choose the greater of the allele name or cell-width-max for the -->
  <!-- standard width -->
  <xsl:variable name="width">
   <xsl:choose>
    <xsl:when test="$cell-width-max &gt; $row-len-max">
     <xsl:value-of select="$cell-width-max"/>
    </xsl:when>
    <xsl:otherwise>
     <xsl:value-of select="$row-len-max"/>
    </xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <!-- calculate the number of cols to fit (subtract one for the row -->
  <!-- allele names) -->
  <xsl:variable name="hardyweinberg-cols-to-fit" 
   select="floor($page-width div $width) - 1"/>

  <!-- check each unique column and output a subtable whenever  -->
  <!-- the column header is a multiple of the cols to fit on the page -->
  <!-- sort by the count (frequency) taken from allelecounts/allele/count -->
  <xsl:for-each select="$unique-cols">
   <xsl:sort select="../count" data-type="number" order="descending"/>   

   <xsl:variable name="pos" select="position()"/>

   <xsl:choose>
    <!-- can fit the max number of cols on page -->
    <xsl:when test="$pos mod $hardyweinberg-cols-to-fit = 0">

     <xsl:variable name="end-col" select="position()"/>
     <xsl:variable name="start-col" 
      select="$end-col - $hardyweinberg-cols-to-fit + 1"/>

     <xsl:call-template name="gen-subtable">
      <xsl:with-param name="node" select="$curr-node"/>
      <xsl:with-param name="start-col" select="$start-col"/>
      <xsl:with-param name="end-col" select="$end-col"/>
      <xsl:with-param name="unique-cols" select="$unique-cols"/>
      <xsl:with-param name="row-len-max" select="$row-len-max"/>
      <xsl:with-param name="col-len-max" select="$width"/>
     </xsl:call-template>

     <xsl:text>                             [Cols: </xsl:text>
     <xsl:value-of select="$start-col"/><xsl:text> to </xsl:text>
     <xsl:value-of select="$end-col"/><xsl:text>]</xsl:text>

    </xsl:when>

    <!-- this deals with the situtation when there are some leftover cols -->
    <xsl:when test="$pos=last() and $pos mod $hardyweinberg-cols-to-fit != 0">
     
     <xsl:variable name="end-col" select="position()"/>
     <xsl:variable name="start-col" 
      select="$end-col - ($pos mod $hardyweinberg-cols-to-fit) + 1"/>

     <xsl:call-template name="gen-subtable">
      <xsl:with-param name="node" select="$curr-node"/>
      <xsl:with-param name="start-col" select="$start-col"/>
      <xsl:with-param name="end-col" select="$end-col"/>
      <xsl:with-param name="unique-cols" select="$unique-cols"/>
      <xsl:with-param name="row-len-max" select="$row-len-max"/>
      <xsl:with-param name="col-len-max" select="$width"/>
     </xsl:call-template>

     <xsl:text>                             [Cols: </xsl:text>
     <xsl:value-of select="$start-col"/><xsl:text> to </xsl:text>
     <xsl:value-of select="$end-col"/><xsl:text>]</xsl:text>

    </xsl:when>
   </xsl:choose>

  </xsl:for-each>

  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template name="gen-subtable">
  <xsl:param name="node"/>
  <xsl:param name="start-col"/>
  <xsl:param name="end-col"/>
  <xsl:param name="unique-cols"/>
  <xsl:param name="row-len-max"/>
  <xsl:param name="col-len-max"/>

  <!-- two loops across allele names, will traverse the matrix -->
  <!-- because we need to use the alleles in count (frequency) order -->
  <!-- don't loop across the <genotype> nodes anymore, we use the loop -->
  <!-- "indicies" to randomly access the given genotype node, using -->
  <!-- a genotype[row,col] format -->


  <xsl:for-each select="$unique-cols">
   <!-- sort by count (frequency) -->
   <xsl:sort select="../count" data-type="number" order="descending"/>   
   <xsl:variable name="row" select="."/>
   <xsl:variable name="row-pos" select="position()"/>
   
   <xsl:for-each select="$unique-cols">
    <!-- sort by count (frequency) -->
    <xsl:sort select="../count" data-type="number" order="descending"/>   
    <xsl:variable name="col" select="."/>
    <xsl:variable name="col-pos" select="position()"/>
    
    <!-- don't generate columns with position greater than the current -->
    <!-- row position, ensures that the matrix remains lower-triangular -->
    <xsl:if test="$col-pos &lt;= $row-pos">
     
     <!-- generate row name, only on first col and only if the row --> 
     <!-- is part of this column processing -->
     
     <xsl:if test="$col-pos=$start-col">
     <xsl:call-template name="newline"/>
     <xsl:call-template name="prepend-pad">
      <xsl:with-param name="length" select="$row-len-max"/>
      <xsl:with-param name="padVar" select="$row"/>
      </xsl:call-template>
     </xsl:if>
     
     <!-- only output cell if in the current column range -->

     <xsl:if test="$col-pos &gt;= $start-col and $col-pos &lt;= $end-col"> 

      <xsl:variable name="cell">

       <!-- "index" into the <genotype> nodes, check both genotype[row,col] -->
       <!-- as well as genotype[col,row], because original genotype XML -->
       <!-- only contains 1/2 * N-squared <genotype> lines, but the matrix -->
       <!-- itself *is* symmetric -->
       <xsl:variable name="genotype" 
	select="$node/genotype[(@row=$row and @col=$col) or 
	(@row=$col and @col=$row)]"/>

       <xsl:value-of select="$genotype/observed"/><xsl:text>/</xsl:text>
       
       <!-- round, format the decimal values of "observed" to nearest 0.1 -->
       <xsl:call-template name="round-to">
	<xsl:with-param name="node" select="$genotype/expected"/>
	<xsl:with-param name="places" select="1"/>
       </xsl:call-template>
      </xsl:variable>
      
      <!-- output cell with padding -->
      <xsl:call-template name="prepend-pad">
       <xsl:with-param name="length" select="$col-len-max"/>
       <xsl:with-param name="padVar" select="$cell"/> 
      </xsl:call-template>
      
     </xsl:if>
    </xsl:if>
    
   </xsl:for-each>

<!-- experimental code to generate lower-triangular matrix for p-vals
     disable for the moment -->

   <xsl:if test="0">

   <xsl:for-each select="$unique-cols">
    <!-- sort by count (frequency) -->
    <xsl:sort select="../count" data-type="number" order="descending"/>    
    <xsl:variable name="col" select="."/>
    <xsl:variable name="col-pos" select="position()"/>
    
    <!-- don't generate columns with position greater than the current -->
    <!-- row position, ensures that the matrix remains lower-triangular -->
    <xsl:if test="$col-pos &lt;= $row-pos">
     
     <!-- generate row name, only on first col and only if the row --> 
     <!-- is part of this column processing -->
     
     <xsl:if test="$col-pos=$start-col">
     <xsl:call-template name="newline"/>
     <xsl:call-template name="prepend-pad">
      <xsl:with-param name="length" select="$row-len-max"/>
      <xsl:with-param name="padVar" select="' '"/>
      </xsl:call-template>
     </xsl:if>
     
     <!-- only output cell if in the current column range -->

     <xsl:if test="$col-pos &gt;= $start-col and $col-pos &lt;= $end-col"> 

      <xsl:variable name="cell">

       <!-- "index" into the <genotype> nodes, check both genotype[row,col] -->
       <!-- as well as genotype[col,row], because original genotype XML -->
       <!-- only contains 1/2 * N-squared <genotype> lines, but the matrix -->
       <!-- itself *is* symmetric -->

       <xsl:call-template name="round-to">
	<xsl:with-param name="node" select="../../../hardyweinbergGuoThompson/pvalue[@type='genotype' and @statistic='chen_statistic' and @row=$row-pos - 1 and @col=$col-pos - 1]"/>
	<xsl:with-param name="places" select="3"/>
       </xsl:call-template>

      </xsl:variable>
      
      <!-- output cell with padding -->
      <xsl:call-template name="prepend-pad">
       <xsl:with-param name="length" select="$col-len-max"/>
       <xsl:with-param name="padVar" select="$cell"/> 
      </xsl:call-template>
      
     </xsl:if>
    </xsl:if>
    
   </xsl:for-each>
   </xsl:if>

  </xsl:for-each>


  <xsl:call-template name="newline"/>

  <!-- indent row for column names-->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$row-len-max"/>
  </xsl:call-template>
  
  <!-- create column footer -->
  <xsl:for-each select="$unique-cols"> 
   <!-- sort by count (frequency) -->
   <xsl:sort select="../count" data-type="number" order="descending" />   
   
   <!-- filter out appropriate subset of columns from unique-column list -->
   <!-- choose the start and end positions of columns *after* sort is -->
   <!-- performed so that reordered positions are consistent with row order -->
   <xsl:if test="position() &gt;= $start-col and position() &lt;= $end-col">
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="length" select="$col-len-max"/>
     <xsl:with-param name="padVar" select="."/>
    </xsl:call-template>
   </xsl:if>

  </xsl:for-each>

  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- print out Guo and Thompson output if it's generated -->
 <xsl:template match="hardyweinbergGuoThompson">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">
      <xsl:text>Guo and Thompson HardyWeinberg output (</xsl:text>
      <xsl:choose>
       <!-- by default we generate MCMC output for the original GT92 test -->
       <xsl:when test="not(@type)">mcmc</xsl:when>
       <xsl:otherwise><xsl:value-of select="@type"/></xsl:otherwise>
      </xsl:choose>
      <xsl:text>)</xsl:text>
      <xsl:choose>
       <xsl:when test="@allelelump=0 or not(@allelelump)"></xsl:when>
       <xsl:otherwise>
	<xsl:text> [lump alleles &lt;= </xsl:text>
	<xsl:value-of select="@allelelump"/>
	<xsl:text>]</xsl:text>
       </xsl:otherwise>
      </xsl:choose>
     </xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="text">
    <xsl:choose>
     <xsl:when test="@role='too-few-alleles'">
      <xsl:text>Too few alleles for 'gthwe' implementation of Guo and Thompson's exact test</xsl:text>
     </xsl:when>
     <xsl:when test="@role='too-large-matrix'">
      <xsl:text>Too large a matrix for 'gthwe' implementation of Guo and Thompson's exact test</xsl:text>
     </xsl:when>
     
     <xsl:otherwise>
      
      <xsl:choose>
       <!-- only when 1 is produced as a pvalue, we return an error -->
       <xsl:when test="normalize-space(pvalue)='1'">
	<xsl:text>Note: p-value is exactly one.</xsl:text>
	<xsl:call-template name="newline"/>
       </xsl:when>
      </xsl:choose>

      <!-- if we are doing MCMC calculate *total steps* to allow comparison with MC-only -->
      <xsl:if test="dememorizationSteps">
       <xsl:text>Total steps in MCMC: </xsl:text>
       <xsl:value-of select="samplingNum * samplingSize"/>
       <xsl:call-template name="newline"/>
      </xsl:if>
      
      <xsl:for-each
       select="stderr|dememorizationSteps|samplingNum|samplingSize|steps">
       <xsl:variable name="node-name" select="name(.)"/>
       <xsl:value-of 
	select="$hw-guo-thompson[@col=$node-name]"/>  
       <xsl:text>: </xsl:text>
       <xsl:value-of select="."/>
       <xsl:call-template name="newline"/>
      </xsl:for-each>
      
      <!-- do pvalue separately -->
      <xsl:value-of select="$hw-guo-thompson[@col='pvalue']"/>  
      <xsl:text> (overall): </xsl:text>
      <xsl:apply-templates select="pvalue[@type='overall']"/>
      <xsl:call-template name="newline"/>

      <xsl:call-template name="indiv-genotypes">
       <xsl:with-param name="pvalues" select="pvalue[@type='genotype']"/>
      </xsl:call-template>

      <!--
      <xsl:text>*switches*</xsl:text>
      <xsl:call-template name="newline"/>
      <xsl:call-template name="linesep-fields">
      <xsl:with-param name="nodes" select="switches/*"/>
     </xsl:call-template>
      -->

     </xsl:otherwise>
     
    </xsl:choose>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <xsl:template name="indiv-genotypes">
  <xsl:param name="pvalues"/>
  <!-- do individual p-values -->
  
  <xsl:variable name="pvals-chen" 
   select="$pvalues[@type='genotype' and @statistic='chen_statistic']"/>
  <xsl:variable name="pvals-diff" 
   select="$pvalues[@type='genotype' and @statistic='diff_statistic']"/>

  <xsl:if test="$pvals-chen or $pvals-diff">
   <xsl:call-template name="newline"/>
   <xsl:text>Individual genotype p-values found to be significant</xsl:text>
   <xsl:call-template name="newline"/>
   <xsl:text>Genotype (observed/expected) [Chen's pval] [diff pval]</xsl:text>
   <xsl:call-template name="newline"/>

   <xsl:choose>
    <xsl:when test="$pvals-chen">
     <xsl:call-template name="gen-genotype-pvals">
      <xsl:with-param name="pvals-loop" select="$pvals-chen"/>
      <xsl:with-param name="pvals-chen" select="$pvals-chen"/>
      <xsl:with-param name="pvals-diff" select="$pvals-diff"/>
     </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
     <xsl:call-template name="gen-genotype-pvals">
      <xsl:with-param name="pvals-loop" select="$pvals-diff"/>
      <xsl:with-param name="pvals-chen" select="$pvals-chen"/>
      <xsl:with-param name="pvals-diff" select="$pvals-diff"/>
     </xsl:call-template>
    </xsl:otherwise>
   </xsl:choose>
  </xsl:if>
 </xsl:template>

 <xsl:template name="gen-genotype-pvals">
  <xsl:param name="pvals-loop"/>
  <xsl:param name="pvals-chen"/>
  <xsl:param name="pvals-diff"/>
  
  <xsl:for-each select="$pvals-loop">
   <xsl:variable name="offset" select="position()"/>
   <xsl:variable name="chen-pval" select="$pvals-chen[$offset]"/>
   <xsl:variable name="diff-pval" select="$pvals-diff[$offset]"/>
   
   <xsl:if test="$chen-pval &lt;= $indiv-geno-pval-cutoff or $diff-pval &lt;= $indiv-geno-pval-cutoff">
    <xsl:variable name="indiv-genotype" 
     select="../genotypetable/genotype[$offset]"/>
    <xsl:value-of select="$indiv-genotype/@row"/>
    <xsl:value-of select="$GL-unphased-genotype-separator"/>
    <xsl:value-of select="$indiv-genotype/@col"/>
    <xsl:text> (</xsl:text>
    <xsl:value-of select="$indiv-genotype/observed"/>
    <xsl:text>/</xsl:text>
    <xsl:value-of select="$indiv-genotype/expected"/>
    <xsl:text>) </xsl:text>
    <xsl:choose>
     <xsl:when test="$chen-pval">
      <xsl:apply-templates select="$chen-pval"/>
     </xsl:when>
     <xsl:otherwise><xsl:text>---</xsl:text></xsl:otherwise>
    </xsl:choose>
    <xsl:text> </xsl:text>
    <xsl:choose>
     <xsl:when test="$diff-pval">
      <xsl:apply-templates select="$diff-pval"/>
     </xsl:when>
     <xsl:otherwise><xsl:text>---</xsl:text></xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="newline"/>
   </xsl:if> 
  </xsl:for-each>
 </xsl:template>

 <!-- print out exact enumeration output if it's generated -->
 <xsl:template match="hardyweinbergEnumeration">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">
      <xsl:text>Exact enumeration HardyWeinberg output</xsl:text>
      <xsl:choose>
       <xsl:when test="@allelelump=0 or not(@allelelump)"></xsl:when>
       <xsl:otherwise>
	<xsl:text> (lump alleles &lt;= </xsl:text>
	<xsl:value-of select="@allelelump"/>
	<xsl:text>)</xsl:text>
       </xsl:otherwise>
      </xsl:choose>
     </xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="text">
    <!-- do pvalue separately -->
    <xsl:text>p-value (overall): </xsl:text>
    <xsl:apply-templates select="pvalue[@type='overall']"/>
    <xsl:call-template name="newline"/>
    <xsl:text>initial observed p-value (overall): </xsl:text>
    <xsl:apply-templates select="pvalue[@type='observed']"/>

    <xsl:call-template name="indiv-genotypes">
     <xsl:with-param name="pvalues" select="pvalue[@type='genotype']"/>
    </xsl:call-template>

   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <xsl:template match="hardyweinbergGuoThompsonArlequin">

  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">Guo and Thompson HardyWeinberg output (Arlequin's implementation)</xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="text">
    <xsl:choose>
     <xsl:when test="@role='monomorphic'">
      <xsl:text>*This locus  is monomorphic: exact test can't be run.*</xsl:text>
     </xsl:when>
     <xsl:otherwise>
	<xsl:for-each
	 select="obs-hetero|exp-hetero|stddev|steps">
       <xsl:variable name="node-name" select="name(.)"/>
       <xsl:value-of select="$hw-guo-thompson-arlequin[@col=$node-name]"/>
       <xsl:text>: </xsl:text>
       <xsl:value-of select="."/>
       <xsl:call-template name="newline"/>
      </xsl:for-each>
      
      <!-- do pvalue separately -->
      <xsl:value-of select="$hw-guo-thompson[@col='pvalue']"/>  
      <xsl:text>: </xsl:text>
      <xsl:apply-templates select="pvalue"/>
      <xsl:call-template name="newline"/>

     </xsl:otherwise>
    </xsl:choose>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <!-- ################  END HARDY-WEINBERG STATISTICS  ############### --> 

</xsl:stylesheet>
<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 
